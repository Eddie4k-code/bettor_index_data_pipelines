"""Read ungraded MLB spreads snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.mlb_team_bet_spreads_grades import MlbTeamBetSpreadsGrade
from db.models.owned.mlb_team_bet_spreads_pregame_snapshots import MlbTeamBetSpreadsPregameSnapshot
from interfaces.mlb_spreads_snapshot_read_repository_interface import MlbSpreadsSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import MlbSpreadsSnapshotRecord


class MlbSpreadsSnapshotReadRepository(MlbSpreadsSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[MlbSpreadsSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=MlbTeamBetSpreadsPregameSnapshot,
            grade_model=MlbTeamBetSpreadsGrade,
            record_cls=MlbSpreadsSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
