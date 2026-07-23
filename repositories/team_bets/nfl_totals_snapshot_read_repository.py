"""Read ungraded NFL totals snapshots for post-game grading."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.owned.nfl_team_bet_totals_grades import NflTeamBetTotalsGrade
from db.models.owned.nfl_team_bet_totals_pregame_snapshots import NflTeamBetTotalsPregameSnapshot
from interfaces.nfl_totals_snapshot_read_repository_interface import NflTotalsSnapshotReadRepositoryInterface
from repositories.team_bets._ungraded_snapshot_reads import fetch_ungraded_snapshots
from schemas.team_bets import NflTotalsSnapshotRecord


class NflTotalsSnapshotReadRepository(NflTotalsSnapshotReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[NflTotalsSnapshotRecord]:
        return fetch_ungraded_snapshots(
            self.db,
            snapshot_model=NflTeamBetTotalsPregameSnapshot,
            grade_model=NflTeamBetTotalsGrade,
            record_cls=NflTotalsSnapshotRecord,
            event_id=event_id,
            as_of=as_of,
        )
