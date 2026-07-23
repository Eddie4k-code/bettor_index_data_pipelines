"""Read ungraded CFB h2h snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.cfb_team_bet_h2h_grades import CfbTeamBetH2hGrade
from db.models.owned.cfb_team_bet_h2h_pregame_snapshots import CfbTeamBetH2hPregameSnapshot
from interfaces.cfb_h2h_snapshot_read_repository_interface import CfbH2hSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import CfbH2hSnapshotRecord


class CfbH2hSnapshotReadRepository(CfbH2hSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[CfbH2hSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=CfbTeamBetH2hPregameSnapshot,
            grade_model=CfbTeamBetH2hGrade,
            record_cls=CfbH2hSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
