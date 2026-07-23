"""Read ungraded NBA spreads snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.nba_team_bet_spreads_grades import NbaTeamBetSpreadsGrade
from db.models.owned.nba_team_bet_spreads_pregame_snapshots import NbaTeamBetSpreadsPregameSnapshot
from interfaces.nba_spreads_snapshot_read_repository_interface import NbaSpreadsSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import NbaSpreadsSnapshotRecord


class NbaSpreadsSnapshotReadRepository(NbaSpreadsSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[NbaSpreadsSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=NbaTeamBetSpreadsPregameSnapshot,
            grade_model=NbaTeamBetSpreadsGrade,
            record_cls=NbaSpreadsSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
