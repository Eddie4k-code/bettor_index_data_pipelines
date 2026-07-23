"""Read ungraded NFL h2h snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.nfl_team_bet_h2h_grades import NflTeamBetH2hGrade
from db.models.owned.nfl_team_bet_h2h_pregame_snapshots import NflTeamBetH2hPregameSnapshot
from interfaces.nfl_h2h_snapshot_read_repository_interface import NflH2hSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import NflH2hSnapshotRecord


class NflH2hSnapshotReadRepository(NflH2hSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[NflH2hSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=NflTeamBetH2hPregameSnapshot,
            grade_model=NflTeamBetH2hGrade,
            record_cls=NflH2hSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
