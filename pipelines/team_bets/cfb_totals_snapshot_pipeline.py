"""CFB totals pregame snapshot orchestrator."""

import logging
from collections.abc import Callable
from datetime import datetime, timezone

from builders.team_bets.totals_snapshot_builder import TotalsSnapshotBuilder
from interfaces.cfb_totals_hit_rate_read_repository_interface import CfbTotalsHitRateReadRepositoryInterface
from interfaces.cfb_totals_snapshot_pipeline_interface import CfbTotalsSnapshotPipelineInterface
from interfaces.cfb_totals_snapshot_repository_interface import CfbTotalsSnapshotRepositoryInterface
from interfaces.featured_odds_read_repository_interface import FeaturedOddsReadRepositoryInterface
from interfaces.team_bet_snapshot_builder_interfaces import TotalsSnapshotBuilderInterface
from schemas.snapshot import SnapshotRequest, SnapshotRunResult

logger = logging.getLogger(__name__)

SPORT_KEY = "americanfootball_ncaaf"
MARKET_KEY = "totals"


class CfbTotalsSnapshotPipeline(CfbTotalsSnapshotPipelineInterface):
    def __init__(
        self,
        *,
        odds_repo: FeaturedOddsReadRepositoryInterface,
        hit_rate_repo: CfbTotalsHitRateReadRepositoryInterface,
        snapshot_repo: CfbTotalsSnapshotRepositoryInterface,
        builder: TotalsSnapshotBuilderInterface | None = None,
        now_fn: Callable[[], datetime] | None = None,
    ):
        self.odds_repo = odds_repo
        self.hit_rate_repo = hit_rate_repo
        self.snapshot_repo = snapshot_repo
        self.builder = builder or TotalsSnapshotBuilder()
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
                f"CfbTotalsSnapshotPipeline requires sport_key={SPORT_KEY!r} and "
                f"market_key={MARKET_KEY!r}, got {request.sport_key!r}/{request.market_key!r}",
            )

        observation_time = request.observation_time
        logger.info(
            "Starting CFB totals snapshot run observation_time=%s",
            observation_time,
        )
        logger.warning(
            "Skipping CFB totals snapshot run: upstream hit-rate tables not available yet",
        )
        return SnapshotRunResult(
            candidates=0,
            snapshotted=0,
            skipped_existing=0,
            skipped_leakage=0,
        )
