"""Read ungraded CFB spreads snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.cfb_team_bet_spreads_grades import CfbTeamBetSpreadsGrade
from db.models.owned.cfb_team_bet_spreads_pregame_snapshots import CfbTeamBetSpreadsPregameSnapshot
from interfaces.cfb_spreads_snapshot_read_repository_interface import CfbSpreadsSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import CfbSpreadsSnapshotRecord


class CfbSpreadsSnapshotReadRepository(CfbSpreadsSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[CfbSpreadsSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=CfbTeamBetSpreadsPregameSnapshot,
            grade_model=CfbTeamBetSpreadsGrade,
            record_cls=CfbSpreadsSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
