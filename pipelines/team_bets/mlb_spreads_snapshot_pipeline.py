"""Mlb Spreads pregame snapshot orchestrator."""

import logging
from collections.abc import Callable
from datetime import datetime, timezone

from builders.team_bets.spreads_snapshot_builder import SpreadsSnapshotBuilder
from interfaces.featured_odds_read_repository_interface import FeaturedOddsReadRepositoryInterface
from interfaces.mlb_spreads_hit_rate_read_repository_interface import MlbSpreadsHitRateReadRepositoryInterface
from interfaces.mlb_spreads_snapshot_pipeline_interface import MlbSpreadsSnapshotPipelineInterface
from interfaces.mlb_spreads_snapshot_repository_interface import MlbSpreadsSnapshotRepositoryInterface
from interfaces.team_bet_snapshot_builder_interfaces import SpreadsSnapshotBuilderInterface
from schemas.snapshot import SnapshotRequest, SnapshotRunResult
from schemas.team_bets import MlbSpreadsSnapshotRecord
from schemas.team_bets.upstream_rows import TeamBetSpreadsHitRateRow

logger = logging.getLogger(__name__)

SPORT_KEY = "baseball_mlb"
MARKET_KEY = "spreads"


class MlbSpreadsSnapshotPipeline(MlbSpreadsSnapshotPipelineInterface):
    def __init__(
        self,
        *,
        odds_repo: FeaturedOddsReadRepositoryInterface,
        hit_rate_repo: MlbSpreadsHitRateReadRepositoryInterface,
        snapshot_repo: MlbSpreadsSnapshotRepositoryInterface,
        builder: SpreadsSnapshotBuilderInterface | None = None,
        now_fn: Callable[[], datetime] | None = None,
    ):
        self.odds_repo = odds_repo
        self.hit_rate_repo = hit_rate_repo
        self.snapshot_repo = snapshot_repo
        self.builder = builder or SpreadsSnapshotBuilder()
        self.now_fn = now_fn or (lambda: datetime.now(timezone.utc))

    def run(self, request: SnapshotRequest) -> SnapshotRunResult:
        if request.sport_key != SPORT_KEY or request.market_key != MARKET_KEY:
            logger.warning(
                "Rejected snapshot request expected sport_key=%s market_key=%s got sport_key=%s market_key=%s",
                SPORT_KEY,
                MARKET_KEY,
                request.sport_key,
                request.market_key,
            )
            raise ValueError(
                f"MlbSpreadsSnapshotPipeline requires sport_key={SPORT_KEY!r} and "
                f"market_key={MARKET_KEY!r}, got {request.sport_key!r}/{request.market_key!r}",
            )

        observation_time = request.observation_time
        logger.info(
            "Starting MLB spreads snapshot run observation_time=%s",
            observation_time,
        )

        odds_rows = self.odds_repo.fetch_pregame_odds(
            sport_key=SPORT_KEY,
            market_key=MARKET_KEY,
            observation_time=observation_time,
        )
        hit_rate_rows = self.hit_rate_repo.fetch_pregame_hit_rates(
            observation_time=observation_time,
        )
        logger.info(
            "Fetched pregame sources observation_time=%s odds_rows=%s hit_rate_rows=%s",
            observation_time,
            len(odds_rows),
            len(hit_rate_rows),
        )

        hit_rate_by_key = _index_hit_rates(hit_rate_rows)

        created_at = self.now_fn()
        snapshotted = 0
        skipped_existing = 0
        skipped_leakage = 0

        for odds in odds_rows:
            join_key = _join_key(odds)
            hit_rate = hit_rate_by_key.get(join_key)
            if hit_rate is None:
                skipped_leakage += 1
                logger.debug(
                    "Skipping odds candidate with no hit rate row event_id=%s bookmaker=%s outcome_name=%s",
                    odds.event_id,
                    odds.bookmaker,
                    odds.outcome_name,
                )
                continue

            record = self.builder.build(
                observation_time=observation_time,
                odds=odds,
                hit_rate=hit_rate,
                record_cls=MlbSpreadsSnapshotRecord,
                created_at=created_at,
            )
            if record is None:
                skipped_leakage += 1
                logger.debug(
                    "Builder rejected odds/hit-rate pair event_id=%s bookmaker=%s outcome_name=%s",
                    odds.event_id,
                    odds.bookmaker,
                    odds.outcome_name,
                )
                continue

            if self.snapshot_repo.insert_if_absent(record):
                snapshotted += 1
                logger.debug(
                    "Snapshotted row event_id=%s bookmaker=%s outcome_name=%s snapshot_version=%s",
                    record.event_id,
                    record.bookmaker,
                    record.outcome_name,
                    record.snapshot_version,
                )
            else:
                skipped_existing += 1
                logger.debug(
                    "Snapshot already exists event_id=%s bookmaker=%s outcome_name=%s snapshot_version=%s",
                    record.event_id,
                    record.bookmaker,
                    record.outcome_name,
                    record.snapshot_version,
                )

        result = SnapshotRunResult(
            candidates=len(odds_rows),
            snapshotted=snapshotted,
            skipped_existing=skipped_existing,
            skipped_leakage=skipped_leakage,
        )
        logger.info(
            "MLB spreads snapshot run complete observation_time=%s candidates=%s snapshotted=%s "
            "skipped_existing=%s skipped_leakage=%s",
            observation_time,
            result.candidates,
            result.snapshotted,
            result.skipped_existing,
            result.skipped_leakage,
        )
        return result


def _join_key(odds) -> tuple[str, str, str, str]:
    return (odds.event_id, odds.bookmaker, odds.market_key, odds.outcome_name)


def _index_hit_rates(
    hit_rate_rows: list[TeamBetSpreadsHitRateRow],
) -> dict[tuple[str, str, str, str], TeamBetSpreadsHitRateRow]:
    return {
        (row.event_id, row.bookmaker, row.market_key, row.outcome_name): row
        for row in hit_rate_rows
    }
