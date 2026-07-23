"""CFB spreads post-game grade orchestrator."""

import logging
from collections.abc import Callable
from datetime import datetime, timezone

from builders.team_bets.spreads_grade_builder import SpreadsGradeBuilder
from interfaces.games_read_repository_interface import GamesReadRepositoryInterface
from interfaces.cfb_spreads_grade_pipeline_interface import CfbSpreadsGradePipelineInterface
from interfaces.cfb_spreads_grade_repository_interface import CfbSpreadsGradeRepositoryInterface
from interfaces.cfb_spreads_snapshot_read_repository_interface import CfbSpreadsSnapshotReadRepositoryInterface
from interfaces.team_bet_grade_builder_interfaces import SpreadsGradeBuilderInterface
from schemas.grade import GradeRequest, GradeRunResult
from schemas.team_bets import CfbSpreadsGradeRecord

logger = logging.getLogger(__name__)

SPORT_KEY = "americanfootball_ncaaf"
MARKET_KEY = "spreads"


class CfbSpreadsGradePipeline(CfbSpreadsGradePipelineInterface):
    def __init__(
        self,
        *,
        snapshot_read_repo: CfbSpreadsSnapshotReadRepositoryInterface,
        games_repo: GamesReadRepositoryInterface,
        grade_repo: CfbSpreadsGradeRepositoryInterface,
        builder: SpreadsGradeBuilderInterface | None = None,
        now_fn: Callable[[], datetime] | None = None,
    ):
        self.snapshot_read_repo = snapshot_read_repo
        self.games_repo = games_repo
        self.grade_repo = grade_repo
        self.builder = builder or SpreadsGradeBuilder()
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
                f"CfbSpreadsGradePipeline requires sport_key={SPORT_KEY!r} and "
                f"market_key={MARKET_KEY!r}, got {request.sport_key!r}/{request.market_key!r}",
            )

        logger.info(
            "Starting CFB spreads grade run event_id=%s",
            request.event_id,
        )
        logger.warning(
            "Skipping CFB spreads grade run: upstream snapshot sources not available yet",
        )
        return GradeRunResult(
            candidates=0,
            graded=0,
            skipped_existing=0,
            skipped_ungradeable=0,
        )
