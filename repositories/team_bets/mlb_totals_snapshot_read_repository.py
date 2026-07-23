"""Read ungraded MLB totals snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.mlb_team_bet_totals_grades import MlbTeamBetTotalsGrade
from db.models.owned.mlb_team_bet_totals_pregame_snapshots import MlbTeamBetTotalsPregameSnapshot
from interfaces.mlb_totals_snapshot_read_repository_interface import MlbTotalsSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import MlbTotalsSnapshotRecord


class MlbTotalsSnapshotReadRepository(MlbTotalsSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[MlbTotalsSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=MlbTeamBetTotalsPregameSnapshot,
            grade_model=MlbTeamBetTotalsGrade,
            record_cls=MlbTotalsSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
