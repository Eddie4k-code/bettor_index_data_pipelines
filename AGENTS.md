# BettorIndex Data Pipelines

## Role

This project builds **clean, reproducible pregame sports betting datasets** for BettorIndex machine learning and model training.

It does **not** ingest odds, compute live hit rates, or serve API responses. That work lives upstream in `revised_engine` and the hit-rate / summarizer workers. This repo **reads** those tables, assembles point-in-time feature rows, grades outcomes after games finish, and exports training-ready datasets.

## Core Rule

**Never use information that became available after the snapshot time when creating a pregame feature.**

Avoid all forms of data leakage. Every feature row must declare an `observation_time` (or equivalent snapshot timestamp). All joins and aggregations must respect that cutoff.

| ✅ Allowed at snapshot time | ❌ Leakage — never use for pregame features |
|------------------------------|---------------------------------------------|
| Odds/lines where `market_last_update <= observation_time` | Final scores, prop stat results, game outcomes |
| Player/team stats from games with `commence_time < bet.commence_time` | Post-game injury updates, line moves after snapshot |
| Hit rates computed from historical games before the slate | Summaries or signals computed with post-game knowledge |
| Bookmaker prices at observation time | Labels used as features (grades belong in label columns only) |

When in doubt, filter explicitly on timestamps — do not rely on implicit table contents alone.

## Pipeline Stages

```text
1. Collect pregame market data
   → read odds + hit-rate rows for upcoming events from shared PostgreSQL

2. Calculate features (pregame only)
   → join at observation_time; enforce temporal filters on every source

3. Save immutable snapshots
   → persist versioned feature rows; never overwrite historical snapshots

4. Grade completed props / team bets after games
   → write outcome labels from post-game stats and scores (separate from features)

5. Export clean datasets
   → Parquet/CSV partitioned for model training and backtesting
```

Each stage should be idempotent and reproducible: same inputs + same `observation_time` → same snapshot.

## Pipeline Position

```text
External APIs (The Odds API, Sports.io / Ball Don't Lie)
        ↓
revised_engine/
  → teams, players, games, player_stats
  → odds_api_props (+ history), odds_api_featured_odds (+ history)
  → hit_rate_event_queue, team_bet_hit_rate_event_queue
        ↓
hit_rate_worker/                         ← prop hit rates (10/30/60 windows)
bettor_index_team_bets_hit_rate_worker/ ← team W-L / cover / totals
        ↓
bettor_index_prop_summarizer_worker/     ← prop signals (derived, not raw features)
bettor_jndex_team_bets_summarizer_worker/ ← team lean summaries (derived)
        ↓
bettorindex_data_pipelines/  (this repo)
  → snapshot pregame features
  → grade outcomes after games
  → export ML / backtest datasets
```

**Legacy path:** `backend/` and `API/` snapshot tables are superseded — read from `revised_engine` tables only.

## Markets in Scope

### Team markets

| `market_key` | Label source |
|--------------|--------------|
| `h2h` | `games` — outright winner |
| `totals` | `games` — combined score vs `outcome_point` |
| `spreads` | `games` — cover vs `outcome_point` |

### Player props

Outcome-centric rows from `{nba,mlb,nfl}_hit_rates`. Grade clears from `{nba,mlb,nfl}_player_stats` (MLB: `mlb_player_stats_ball_dont_lie`) matched on `market_key`, `outcome_point`, and player identity.

Prop `market_key` values follow upstream ingestion — see `revised_engine/scripts/nfl_market_config.py` for NFL registry.

## Sport Keys

Use canonical keys from `revised_engine/sport_keys.py`:

| Sport | `sport_key` | Table prefix |
|-------|-------------|--------------|
| NBA | `basketball_nba` | `nba_` |
| MLB | `baseball_mlb` | `mlb_` |
| NFL | `americanfootball_nfl` | `nfl_` |

Route by `sport_key`; normalize aliases via `normalize_sport_key()`.

**Completed game statuses** (for grading only): `finished` (NBA), `status_final` (MLB), `final` (NFL).

## Data Sources (Read-Only)

All services share PostgreSQL via `DATABASE_URL`.

| Layer | Tables |
|-------|--------|
| Foundation | `teams`, `player`, `games`, `{nba,mlb,nfl}_player_stats*` |
| Odds (current + history) | `odds_api_props`, `odds_api_props_history`, `odds_api_featured_odds`, `odds_api_featured_odds_history` |
| Prop features | `{nba,mlb,nfl}_hit_rates` |
| Team features | `{sport}_team_bet_{,totals_,spreads_}hit_rates` |
| Grading (owned by this repo) | `{sport}_team_bet_{h2h,spreads,totals}_grades` |
| Snapshots (owned by this repo) | `{sport}_team_bet_{h2h,spreads,totals}_pregame_snapshots` |

**Feature sources:** hit-rate tables + raw stats/odds. Summaries and signals (`{sport}_summaries`, lean columns) are downstream derivatives — use with care; prefer raw hit-rate and odds columns for ML features unless the snapshot time of the summary is proven pregame.

**Bookmakers in scope:** `draftkings`, `fanduel`, `betmgm`, `fanatics` (match upstream).

## Snapshot Contract

Every persisted snapshot row should carry:

| Field | Purpose |
|-------|---------|
| `observation_time` | Cutoff for all feature joins |
| `event_id`, `sport_key`, `market_key` | Identity |
| `bookmaker`, `outcome_name`, `outcome_point`, `outcome_price` | Market state at snapshot |
| Feature columns | Typed, explicit — no opaque JSON blobs unless schema-versioned |
| `snapshot_version` or content hash | Reproducibility and audit |

Rules:

- Snapshots are **append-only** — corrections get a new row/version, not an in-place update.
- One snapshot captures one observable market state; multiple observation times per event are expected (e.g. T-24h, T-1h, close).
- Grades are written **after** the game completes, in separate tables/columns — never merged back into historical snapshot rows.

## Grading Contract

Grades are labels, not features. Write them only once the game is complete and stats/scores are available.

### Grade row primary key (export join to snapshots)

Match snapshot PK on:

| Column | Purpose |
|--------|---------|
| `observation_time` | Links to the snapshotted feature row |
| `event_id` | Event identity |
| `bookmaker` | Book scope |
| `outcome_name` | Side picked (team name or Over/Under) |
| `snapshot_version` | Feature schema version (e.g. `nba_h2h_v1`) |

Export join: `snapshots.* = grades.*` on these five columns.

### Label columns

| Column | Purpose |
|--------|---------|
| `grade_outcome` | `win` \| `loss` \| `push` \| `void` |
| `grade_version` | Grading logic version (e.g. `nba_h2h_grade_v1`) |
| `home_team_score`, `away_team_score` | Scores used to compute the label |
| `outcome_point` | Line from snapshot (spreads/totals push logic) |
| `commence_time` | From snapshot (partitioning / export) |
| `graded_at`, `created_at` | Audit timestamps |

Shared types live in `schemas/grade.py` (`GradeRequest`, `GradeRunResult`, `GradeOutcome`).

### Grade logic

| Market type | Grade logic |
|-------------|-------------|
| Player props | Compare stat value vs line (`outcome_point`); handle push, DNP, void rules per sport |
| `h2h` | Outcome team score vs opponent (`win` / `loss` / `push` on tie) |
| `totals` | Over/under vs combined score |
| `spreads` | Cover vs handicap; push when margin is zero |

Completed game statuses for grading: `finished` (NBA), `status_final` (MLB), `final` (NFL).

Align grade PKs with snapshot row keys so exports join features → labels cleanly. Grades are append-only; one grade row per snapshot row for v1.

## Export Contract

Exports are derived from snapshots + grades — never from live mutable tables alone.

Suggested layout:

```text
exports/{sport_key}/{market_key}/{observation_date}/
  features.parquet
  labels.parquet          # optional separate file
  manifest.json           # row counts, snapshot_version, git SHA, filters applied
```

Include metadata sufficient to reproduce the export: `observation_time` range, sport/market filters, schema version.

## Architecture

```text
main.py                  # CLI entrypoint (snapshot, grade, export commands)
pipelines/team_bets/     # 12 snapshot + 12 grade orchestrators (explicit per sport×market)
builders/team_bets/      # Shared h2h / spreads / totals snapshot + grade builders
repositories/            # Upstream reads + owned snapshot/grade reads and writes
interfaces/              # ABC for every external boundary
schemas/                 # Pydantic snapshot/grade records and request/result types
db/models/               # SQLAlchemy models for snapshot + grade tables only
tests/                   # pytest; write failing test first (TDD)
```

Design rules (mirror `hit_rate_worker/.cursor/rules/solid-tdd.mdc`):

- Depend on interfaces, not concrete classes
- Read upstream tables through repositories — no duplicated ingestion or hit-rate math
- Mock dependencies in unit tests — no real DB or API calls in unit tests
- One pipeline per stage; explicit temporal filters in repository queries
- No pointless one-line helper functions

## Anti-Leakage Checklist

Before merging any feature or export code, verify:

1. **Stats:** only games with `commence_time < event.commence_time` (strict `<`, not `<=` unless documented).
2. **Odds:** use history table or current row with `market_last_update <= observation_time`.
3. **Hit rates:** confirm upstream computation used only pre-slate history (see worker AGENTS.md); snapshot at a fixed `observation_time`.
4. **Labels:** grades reference post-game data only in label columns/files, never in feature columns.
5. **Exports:** training splits by `commence_time` or `observation_time`, not random row shuffle across time.
6. **Tests:** include cases where a post-game stat or line move exists in DB but must be **excluded** from the snapshot.

## Reference Implementations

| Concern | Reference |
|---------|-----------|
| Sport key normalization | `revised_engine/sport_keys.py` |
| Props ingestion + history | `revised_engine/pipelines/props_pipeline.py` |
| Team odds ingestion | `revised_engine/pipelines/featured_odds_pipeline.py` |
| Completed games only | `revised_engine/pipelines/games_pipeline.py` |
| Prop hit rates + windows | `hit_rate_worker/` |
| Team hit rates + windows | `bettor_index_team_bets_hit_rate_worker/AGENTS.md` |
| Team window sizes | `bettor_index_team_bets_hit_rate_worker/analytics/sport_windows.py` |
| Prop signal shape (derived) | `bettor_index_prop_summarizer_worker/docs/bettorindexpropsignals.md` |
| Point-in-time / `as_of` pattern | `line_movement_worker/` |
| Pipeline validation SQL | `bettor_jndex_team_bets_summarizer_worker/.cursor/skills/betting-pipeline-validation/reference.md` |
| NFL market registry | `revised_engine/scripts/nfl_market_config.py` |
| TDD / SOLID conventions | `hit_rate_worker/.cursor/rules/solid-tdd.mdc` |

## Run & Test

```bash
pip install -r requirements.txt
pytest
python main.py --help          # snapshot | grade | export subcommands
python main.py grade nba-h2h   # optional --event-id filter
```

## Out of Scope

- Odds ingestion, featured odds storage, or line-movement detection (`revised_engine`, `line_movement_worker`)
- Computing hit rates from game history (`hit_rate_worker`, `bettor_index_team_bets_hit_rate_worker`)
- Prop or team summarization / lean signals (`bettor_index_prop_summarizer_worker`, `bettor_jndex_team_bets_summarizer_worker`)
- REST API exposure (`bettor_index_rest_Api`)
- Legacy `backend/` / `API/` snapshot tables
- Live inference or model training — this repo prepares datasets only

## Before Adding a Sport, Market, or Export

Clarify if not already decided:

1. Exact `sport_key` and table prefix
2. Which upstream hit-rate and odds tables to join
3. Snapshot observation schedule (e.g. close, T-1h, custom)
4. Grading rules for push, void, DNP, overtime
5. Export schema version and partition strategy
