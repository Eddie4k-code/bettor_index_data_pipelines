"""NBA moneyline pregame snapshot orchestrator."""

from collections.abc import Callable
from datetime import datetime, timezone

from builders.team_bets.h2h_snapshot_builder import H2hSnapshotBuilder
from interfaces.featured_odds_read_repository_interface import FeaturedOddsReadRepositoryInterface
from interfaces.nba_h2h_hit_rate_read_repository_interface import NbaH2hHitRateReadRepositoryInterface
from interfaces.nba_h2h_snapshot_pipeline_interface import NbaH2hSnapshotPipelineInterface
from interfaces.nba_h2h_snapshot_repository_interface import NbaH2hSnapshotRepositoryInterface
from interfaces.team_bet_snapshot_builder_interfaces import H2hSnapshotBuilderInterface
from schemas.snapshot import SnapshotRequest, SnapshotRunResult
from schemas.team_bets import NbaH2hSnapshotRecord
from schemas.team_bets.upstream_rows import TeamBetH2hHitRateRow

SPORT_KEY = "basketball_nba"
MARKET_KEY = "h2h"


class NbaH2hSnapshotPipeline(NbaH2hSnapshotPipelineInterface):
    def __init__(
        self,
        *,
        odds_repo: FeaturedOddsReadRepositoryInterface,
        hit_rate_repo: NbaH2hHitRateReadRepositoryInterface,
        snapshot_repo: NbaH2hSnapshotRepositoryInterface,
        builder: H2hSnapshotBuilderInterface | None = None,
        now_fn: Callable[[], datetime] | None = None,
    ):
        self.odds_repo = odds_repo
        self.hit_rate_repo = hit_rate_repo
        self.snapshot_repo = snapshot_repo
        self.builder = builder or H2hSnapshotBuilder()
        self.now_fn = now_fn or (lambda: datetime.now(timezone.utc))

    def run(self, request: SnapshotRequest) -> SnapshotRunResult:
        if request.sport_key != SPORT_KEY or request.market_key != MARKET_KEY:
            raise ValueError(
                f"NbaH2hSnapshotPipeline requires sport_key={SPORT_KEY!r} and "
                f"market_key={MARKET_KEY!r}, got {request.sport_key!r}/{request.market_key!r}",
            )

        observation_time = request.observation_time
        odds_rows = self.odds_repo.fetch_pregame_odds(
            sport_key=SPORT_KEY,
            market_key=MARKET_KEY,
            observation_time=observation_time,
        )
        hit_rate_rows = self.hit_rate_repo.fetch_pregame_hit_rates(
            observation_time=observation_time,
        )
        hit_rate_by_key = _index_hit_rates(hit_rate_rows)

        created_at = self.now_fn()
        snapshotted = 0
        skipped_existing = 0
        skipped_leakage = 0

        for odds in odds_rows:
            hit_rate = hit_rate_by_key.get(_join_key(odds))
            if hit_rate is None:
                skipped_leakage += 1
                continue

            record = self.builder.build(
                observation_time=observation_time,
                odds=odds,
                hit_rate=hit_rate,
                record_cls=NbaH2hSnapshotRecord,
                created_at=created_at,
            )
            if record is None:
                skipped_leakage += 1
                continue

            if self.snapshot_repo.insert_if_absent(record):
                snapshotted += 1
            else:
                skipped_existing += 1

        return SnapshotRunResult(
            candidates=len(odds_rows),
            snapshotted=snapshotted,
            skipped_existing=skipped_existing,
            skipped_leakage=skipped_leakage,
        )


def _join_key(odds) -> tuple[str, str, str, str]:
    return (odds.event_id, odds.bookmaker, odds.market_key, odds.outcome_name)


def _index_hit_rates(
    hit_rate_rows: list[TeamBetH2hHitRateRow],
) -> dict[tuple[str, str, str, str], TeamBetH2hHitRateRow]:
    return {
        (row.event_id, row.bookmaker, row.market_key, row.outcome_name): row
        for row in hit_rate_rows
    }
