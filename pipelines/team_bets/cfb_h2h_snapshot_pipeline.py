"""CFB moneyline pregame snapshot orchestrator."""

import logging
from collections.abc import Callable
from datetime import datetime, timezone

from builders.team_bets.h2h_snapshot_builder import H2hSnapshotBuilder
from interfaces.cfb_h2h_hit_rate_read_repository_interface import CfbH2hHitRateReadRepositoryInterface
from interfaces.cfb_h2h_snapshot_pipeline_interface import CfbH2hSnapshotPipelineInterface
from interfaces.cfb_h2h_snapshot_repository_interface import CfbH2hSnapshotRepositoryInterface
from interfaces.featured_odds_read_repository_interface import FeaturedOddsReadRepositoryInterface
from interfaces.team_bet_snapshot_builder_interfaces import H2hSnapshotBuilderInterface
from schemas.snapshot import SnapshotRequest, SnapshotRunResult

logger = logging.getLogger(__name__)

SPORT_KEY = "americanfootball_ncaaf"
MARKET_KEY = "h2h"


class CfbH2hSnapshotPipeline(CfbH2hSnapshotPipelineInterface):
    def __init__(
        self,
        *,
        odds_repo: FeaturedOddsReadRepositoryInterface,
        hit_rate_repo: CfbH2hHitRateReadRepositoryInterface,
        snapshot_repo: CfbH2hSnapshotRepositoryInterface,
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
            logger.warning(
                "Rejected snapshot request expected sport_key=%s market_key=%s got sport_key=%s market_key=%s",
                SPORT_KEY,
                MARKET_KEY,
                request.sport_key,
                request.market_key,
            )
            raise ValueError(
                f"CfbH2hSnapshotPipeline requires sport_key={SPORT_KEY!r} and "
                f"market_key={MARKET_KEY!r}, got {request.sport_key!r}/{request.market_key!r}",
            )

        observation_time = request.observation_time
        logger.info(
            "Starting CFB H2H snapshot run observation_time=%s",
            observation_time,
        )
        logger.warning(
            "Skipping CFB H2H snapshot run: upstream hit-rate tables not available yet",
        )
        return SnapshotRunResult(
            candidates=0,
            snapshotted=0,
            skipped_existing=0,
            skipped_leakage=0,
        )
