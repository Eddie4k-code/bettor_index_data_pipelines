"""Read ungraded NBA totals snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.nba_team_bet_totals_grades import NbaTeamBetTotalsGrade
from db.models.owned.nba_team_bet_totals_pregame_snapshots import NbaTeamBetTotalsPregameSnapshot
from interfaces.nba_totals_snapshot_read_repository_interface import NbaTotalsSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import NbaTotalsSnapshotRecord


class NbaTotalsSnapshotReadRepository(NbaTotalsSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[NbaTotalsSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=NbaTeamBetTotalsPregameSnapshot,
            grade_model=NbaTeamBetTotalsGrade,
            record_cls=NbaTotalsSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
