"""CFB totals post-game grade orchestrator."""

import logging
from collections.abc import Callable
from datetime import datetime, timezone

from builders.team_bets.totals_grade_builder import TotalsGradeBuilder
from interfaces.games_read_repository_interface import GamesReadRepositoryInterface
from interfaces.cfb_totals_grade_pipeline_interface import CfbTotalsGradePipelineInterface
from interfaces.cfb_totals_grade_repository_interface import CfbTotalsGradeRepositoryInterface
from interfaces.cfb_totals_snapshot_read_repository_interface import CfbTotalsSnapshotReadRepositoryInterface
from interfaces.team_bet_grade_builder_interfaces import TotalsGradeBuilderInterface
from schemas.grade import GradeRequest, GradeRunResult
from schemas.team_bets import CfbTotalsGradeRecord

logger = logging.getLogger(__name__)

SPORT_KEY = "americanfootball_ncaaf"
MARKET_KEY = "totals"


class CfbTotalsGradePipeline(CfbTotalsGradePipelineInterface):
    def __init__(
        self,
        *,
        snapshot_read_repo: CfbTotalsSnapshotReadRepositoryInterface,
        games_repo: GamesReadRepositoryInterface,
        grade_repo: CfbTotalsGradeRepositoryInterface,
        builder: TotalsGradeBuilderInterface | None = None,
        now_fn: Callable[[], datetime] | None = None,
    ):
        self.snapshot_read_repo = snapshot_read_repo
        self.games_repo = games_repo
        self.grade_repo = grade_repo
        self.builder = builder or TotalsGradeBuilder()
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
                f"CfbTotalsGradePipeline requires sport_key={SPORT_KEY!r} and "
                f"market_key={MARKET_KEY!r}, got {request.sport_key!r}/{request.market_key!r}",
            )

        logger.info(
            "Starting CFB totals grade run event_id=%s",
            request.event_id,
        )
        logger.warning(
            "Skipping CFB totals grade run: upstream snapshot sources not available yet",
        )
        return GradeRunResult(
            candidates=0,
            graded=0,
            skipped_existing=0,
            skipped_ungradeable=0,
        )
