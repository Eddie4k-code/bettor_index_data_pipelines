"""CFB H2H post-game grade orchestrator."""

import logging
from collections.abc import Callable
from datetime import datetime, timezone

from builders.team_bets.h2h_grade_builder import H2hGradeBuilder
from interfaces.games_read_repository_interface import GamesReadRepositoryInterface
from interfaces.cfb_h2h_grade_pipeline_interface import CfbH2hGradePipelineInterface
from interfaces.cfb_h2h_grade_repository_interface import CfbH2hGradeRepositoryInterface
from interfaces.cfb_h2h_snapshot_read_repository_interface import CfbH2hSnapshotReadRepositoryInterface
from interfaces.team_bet_grade_builder_interfaces import H2hGradeBuilderInterface
from schemas.grade import GradeRequest, GradeRunResult
from schemas.team_bets import CfbH2hGradeRecord

logger = logging.getLogger(__name__)

SPORT_KEY = "americanfootball_ncaaf"
MARKET_KEY = "h2h"


class CfbH2hGradePipeline(CfbH2hGradePipelineInterface):
    def __init__(
        self,
        *,
        snapshot_read_repo: CfbH2hSnapshotReadRepositoryInterface,
        games_repo: GamesReadRepositoryInterface,
        grade_repo: CfbH2hGradeRepositoryInterface,
        builder: H2hGradeBuilderInterface | None = None,
        now_fn: Callable[[], datetime] | None = None,
    ):
        self.snapshot_read_repo = snapshot_read_repo
        self.games_repo = games_repo
        self.grade_repo = grade_repo
        self.builder = builder or H2hGradeBuilder()
        self.now_fn = now_fn or (lambda: datetime.now(timezone.utc))

    def run(self, request: GradeRequest) -> GradeRunResult:
        if request.sport_key != SPORT_KEY or request.market_key != MARKET_KEY:
            logger.warning(
                "Rejected grade request expected sport_key=%s market_key=%s got sport_key=%s market_key=%s",
                SPORT_KEY,
                MARKET_KEY,
                request.sport_key,
                request.market_key,
            )
            raise ValueError(
                f"CfbH2hGradePipeline requires sport_key={SPORT_KEY!r} and "
                f"market_key={MARKET_KEY!r}, got {request.sport_key!r}/{request.market_key!r}",
            )

        logger.info(
            "Starting CFB H2H grade run event_id=%s",
            request.event_id,
        )
        logger.warning(
            "Skipping CFB H2H grade run: upstream snapshot sources not available yet",
        )
        return GradeRunResult(
            candidates=0,
            graded=0,
            skipped_existing=0,
            skipped_ungradeable=0,
        )
