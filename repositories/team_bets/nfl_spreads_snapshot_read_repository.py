"""Read ungraded NFL spreads snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.nfl_team_bet_spreads_grades import NflTeamBetSpreadsGrade
from db.models.owned.nfl_team_bet_spreads_pregame_snapshots import NflTeamBetSpreadsPregameSnapshot
from interfaces.nfl_spreads_snapshot_read_repository_interface import NflSpreadsSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import NflSpreadsSnapshotRecord


class NflSpreadsSnapshotReadRepository(NflSpreadsSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[NflSpreadsSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=NflTeamBetSpreadsPregameSnapshot,
            grade_model=NflTeamBetSpreadsGrade,
            record_cls=NflSpreadsSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
