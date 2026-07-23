"""Read ungraded NBA h2h snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.nba_team_bet_h2h_grades import NbaTeamBetH2hGrade
from db.models.owned.nba_team_bet_h2h_pregame_snapshots import NbaTeamBetH2hPregameSnapshot
from interfaces.nba_h2h_snapshot_read_repository_interface import NbaH2hSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import NbaH2hSnapshotRecord


class NbaH2hSnapshotReadRepository(NbaH2hSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[NbaH2hSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=NbaTeamBetH2hPregameSnapshot,
            grade_model=NbaTeamBetH2hGrade,
            record_cls=NbaH2hSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
