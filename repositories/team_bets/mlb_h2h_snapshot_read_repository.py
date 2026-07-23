"""Read ungraded MLB h2h snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.mlb_team_bet_h2h_grades import MlbTeamBetH2hGrade
from db.models.owned.mlb_team_bet_h2h_pregame_snapshots import MlbTeamBetH2hPregameSnapshot
from interfaces.mlb_h2h_snapshot_read_repository_interface import MlbH2hSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import MlbH2hSnapshotRecord


class MlbH2hSnapshotReadRepository(MlbH2hSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[MlbH2hSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=MlbTeamBetH2hPregameSnapshot,
            grade_model=MlbTeamBetH2hGrade,
            record_cls=MlbH2hSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
