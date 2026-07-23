"""MLB H2H post-game grade orchestrator."""

import logging
from collections.abc import Callable
from datetime import datetime, timezone

from builders.team_bets.h2h_grade_builder import H2hGradeBuilder
from interfaces.games_read_repository_interface import GamesReadRepositoryInterface
from interfaces.mlb_h2h_grade_pipeline_interface import MlbH2hGradePipelineInterface
from interfaces.mlb_h2h_grade_repository_interface import MlbH2hGradeRepositoryInterface
from interfaces.mlb_h2h_snapshot_read_repository_interface import MlbH2hSnapshotReadRepositoryInterface
from interfaces.team_bet_grade_builder_interfaces import H2hGradeBuilderInterface
from schemas.grade import GradeRequest, GradeRunResult
from schemas.team_bets import MlbH2hGradeRecord

logger = logging.getLogger(__name__)

SPORT_KEY = "baseball_mlb"
MARKET_KEY = "h2h"


class MlbH2hGradePipeline(MlbH2hGradePipelineInterface):
    def __init__(
        self,
        *,
        snapshot_read_repo: MlbH2hSnapshotReadRepositoryInterface,
        games_repo: GamesReadRepositoryInterface,
        grade_repo: MlbH2hGradeRepositoryInterface,
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
                f"MlbH2hGradePipeline requires sport_key={SPORT_KEY!r} and "
                f"market_key={MARKET_KEY!r}, got {request.sport_key!r}/{request.market_key!r}",
            )

        now = self.now_fn()
        logger.info(
            "Starting MLB H2H grade run event_id=%s",
            request.event_id,
        )

        candidates = self.snapshot_read_repo.fetch_ungraded_candidates(
            event_id=request.event_id,
            as_of=now,
        )
        logger.info(
            "Fetched ungraded snapshot candidates count=%s",
            len(candidates),
        )

        graded_at = now
        created_at = now
        graded = 0
        skipped_existing = 0
        skipped_ungradeable = 0

        for snapshot in candidates:
            if snapshot.home_team_id is None or snapshot.away_team_id is None:
                skipped_ungradeable += 1
                logger.debug(
                    "Skipping snapshot with missing team ids event_id=%s bookmaker=%s outcome_name=%s",
                    snapshot.event_id,
                    snapshot.bookmaker,
                    snapshot.outcome_name,
                )
                continue

            game = self.games_repo.fetch_completed_game(
                sport_key=SPORT_KEY,
                event_id=snapshot.event_id,
                home_team_id=snapshot.home_team_id,
                away_team_id=snapshot.away_team_id,
                commence_time=snapshot.commence_time,
            )
            if game is None:
                skipped_ungradeable += 1
                logger.debug(
                    "Skipping snapshot with no completed game event_id=%s bookmaker=%s outcome_name=%s",
                    snapshot.event_id,
                    snapshot.bookmaker,
                    snapshot.outcome_name,
                )
                continue

            record = self.builder.build(
                snapshot=snapshot,
                game=game,
                record_cls=MlbH2hGradeRecord,
                graded_at=graded_at,
                created_at=created_at,
            )
            if record is None:
                skipped_ungradeable += 1
                logger.debug(
                    "Builder rejected snapshot event_id=%s bookmaker=%s outcome_name=%s",
                    snapshot.event_id,
                    snapshot.bookmaker,
                    snapshot.outcome_name,
                )
                continue

            if self.grade_repo.insert_if_absent(record):
                graded += 1
                logger.debug(
                    "Graded row event_id=%s bookmaker=%s outcome_name=%s grade_outcome=%s",
                    record.event_id,
                    record.bookmaker,
                    record.outcome_name,
                    record.grade_outcome,
                )
            else:
                skipped_existing += 1
                logger.debug(
                    "Grade already exists event_id=%s bookmaker=%s outcome_name=%s",
                    record.event_id,
                    record.bookmaker,
                    record.outcome_name,
                )

        result = GradeRunResult(
            candidates=len(candidates),
            graded=graded,
            skipped_existing=skipped_existing,
            skipped_ungradeable=skipped_ungradeable,
        )
        logger.info(
            "MLB H2H grade run complete event_id=%s candidates=%s graded=%s "
            "skipped_existing=%s skipped_ungradeable=%s",
            request.event_id,
            result.candidates,
            result.graded,
            result.skipped_existing,
            result.skipped_ungradeable,
        )
        return result
