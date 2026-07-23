"""Read ungraded CFB totals snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.cfb_team_bet_totals_grades import CfbTeamBetTotalsGrade
from db.models.owned.cfb_team_bet_totals_pregame_snapshots import CfbTeamBetTotalsPregameSnapshot
from interfaces.cfb_totals_snapshot_read_repository_interface import CfbTotalsSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import CfbTotalsSnapshotRecord


class CfbTotalsSnapshotReadRepository(CfbTotalsSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[CfbTotalsSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=CfbTeamBetTotalsPregameSnapshot,
            grade_model=CfbTeamBetTotalsGrade,
            record_cls=CfbTotalsSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
