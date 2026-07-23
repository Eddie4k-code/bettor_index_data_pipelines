# BettorIndex Data Pipelines

Build **clean, reproducible pregame sports betting datasets** for BettorIndex machine learning and model training.

This repo reads shared PostgreSQL tables populated by upstream ingestion and hit-rate workers, assembles point-in-time feature rows, persists immutable snapshots, and writes post-game labels after games finish. Export (training Parquet/CSV) is the next stage.

## What this repo does

| Stage | Status | Description |
|-------|--------|-------------|
| **Snapshot** | Implemented | Join pregame odds + hit rates at a fixed `observation_time`; write append-only feature rows |
| **Grade** | Implemented | Write win/loss/push labels after games finish (separate from features) |
| **Export** | Planned | Join snapshots + grades into partitioned training datasets |

## What this repo does not do

- Ingest odds, games, or stats (`revised_engine`)
- Compute hit rates (`hit_rate_worker`, `bettor_index_team_bets_hit_rate_worker`)
- Serve REST API responses
- Train or run live inference models

See [AGENTS.md](./AGENTS.md) for full architecture contracts, anti-leakage rules, and contributor guidance.

## Position in the BettorIndex stack

```text
External APIs (The Odds API, Sports.io / Ball Don't Lie)
        ↓
revised_engine/          → teams, games, odds, player stats
        ↓
hit_rate_worker/           → prop hit rates
bettor_index_team_bets_hit_rate_worker/  → team W-L / cover / totals hit rates
        ↓
bettorindex_data_pipelines/  (this repo)
  → snapshot pregame features
  → grade outcomes
  → export ML datasets (planned)
```

## Supported team-bet snapshots

Four sports × three markets = **12 explicit snapshot and grade pipelines**, each with its own pipeline class, repositories, owned tables, and CLI subcommands.

| Sport | `sport_key` | Markets | CLI examples |
|-------|-------------|---------|--------------|
| NBA | `basketball_nba` | h2h, spreads, totals | `snapshot nba-h2h`, `grade nba-h2h`, … |
| MLB | `baseball_mlb` | h2h, spreads, totals | `snapshot mlb-h2h`, `grade mlb-h2h`, … |
| NFL | `americanfootball_nfl` | h2h, spreads, totals | `snapshot nfl-h2h`, `grade nfl-h2h`, … |
| CFB | `americanfootball_ncaaf` | h2h, spreads, totals | `snapshot cfb-h2h`, `grade cfb-h2h`, … |

**CFB note:** Pipelines and owned tables exist, but CFB snapshot and grade runs currently log and return zero counts until upstream `cfb_team_bet_*_hit_rates` tables are available. NBA, MLB, and NFL are fully runnable against PostgreSQL.

**Bookmakers in scope:** `draftkings`, `fanduel`, `betmgm`, `fanatics`

## Quick start

### Prerequisites

- Python 3.11+
- PostgreSQL with BettorIndex upstream tables (`revised_engine`, hit-rate workers)
- `DATABASE_URL` pointing at the shared database

### Install

```bash
pip install -r requirements.txt
```

### Configure

Create a `.env` file in the project root:

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/bettorindex
```

Owned snapshot and grade tables are created automatically on first CLI run.

### Run a snapshot

```bash
python main.py snapshot nba-h2h --observation-time 2026-07-21T12:00:00Z
```

`--observation-time` accepts ISO-8601 timestamps (e.g. `2026-07-21T08:00:00-04:00` or `…Z`). This is the cutoff for all pregame joins: odds and hit rates must be observable at or before this time, and the game must not have started yet.

Example output:

```text
Snapshot complete candidates=42 snapshotted=38 skipped_existing=0 skipped_leakage=4
```

List all snapshot subcommands:

```bash
python main.py snapshot --help
```

### Run a grade

After games finish, write post-game labels for snapshot rows that lack a grade:

```bash
python main.py grade nba-h2h
python main.py grade nfl-spreads --event-id abc123eventid
```

Example output:

```text
Grade complete candidates=38 graded=36 skipped_existing=0 skipped_ungradeable=2
```

Grades join to snapshots on `(observation_time, event_id, bookmaker, outcome_name, snapshot_version)` and store `grade_outcome` as `win`, `loss`, `push`, or `void`.

List all grade subcommands:

```bash
python main.py grade --help
```

## How snapshots work

Each snapshot row captures one observable market state at `observation_time`:

1. **Odds** — from `odds_api_featured_odds` where `market_last_update <= observation_time` and `commence_time > observation_time`
2. **Hit rates** — from `{sport}_team_bet_{,spreads_,totals_}hit_rates` with matching temporal filters and line alignment
3. **Features** — market-specific windows (W/L for h2h, cover for spreads, clear for totals)
4. **Persistence** — append-only writes to owned `{sport}_team_bet_{market}_pregame_snapshots` tables; duplicate keys are skipped

**Anti-leakage:** Features never use final scores, post-game stats, or line moves after `observation_time`. Grades live in separate `{sport}_team_bet_{market}_grades` tables and are joined only at export time.

## How grades work

Each grade pipeline:

1. **Candidates** — owned snapshot rows with `commence_time <= now` and no matching grade PK
2. **Game lookup** — final scores from shared `games` (matchup + commence window)
3. **Label** — shared h2h / spreads / totals builders compute `win` / `loss` / `push`
4. **Persistence** — append-only writes to owned grade tables; duplicate keys are skipped

## Project structure

```text
main.py                     # CLI: snapshot + grade subcommands (export planned)
pipelines/team_bets/        # One snapshot + grade orchestrator per sport×market (24 pipelines)
builders/team_bets/         # Shared h2h / spreads / totals snapshot + grade builders
repositories/               # Upstream reads + owned snapshot/grade reads and writes
interfaces/                 # ABCs for repos, pipelines, builders
schemas/                    # Pydantic snapshot/grade records and request/result types
db/models/
  upstream/                 # Read-only ORM mirrors of shared tables
  owned/                    # Snapshot + grade tables owned by this repo
tests/                      # pytest (mocked deps; no real DB in unit tests)
```

Design follows SOLID + TDD: depend on interfaces, inject repositories, write failing tests first. See [.cursor/rules/solid-tdd.mdc](./.cursor/rules/solid-tdd.mdc).

## Development

```bash
pytest                    # full suite
pytest tests/test_main_cli.py -v
python main.py --help
```

For deeper contracts (grading rules, export layout, sport key normalization, reference implementations), read [AGENTS.md](./AGENTS.md).

## Roadmap

- [x] Team-bet snapshot pipelines for NBA, MLB, NFL, CFB (12 types)
- [x] CLI snapshot subcommands
- [x] Grade pipelines (post-game labels from `games`)
- [x] CLI grade subcommands
- [ ] Export pipelines (Parquet/CSV partitioned by sport, market, observation date)
- [ ] Player prop snapshots (separate vertical slices)
