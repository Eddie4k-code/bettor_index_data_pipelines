"""Append-only writes to ``mlb_team_bet_totals_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.mlb_team_bet_totals_pregame_snapshots import MlbTeamBetTotalsPregameSnapshot
from interfaces.mlb_totals_snapshot_repository_interface import MlbTotalsSnapshotRepositoryInterface
from schemas.team_bets import MlbTotalsSnapshotRecord


class MlbTotalsSnapshotRepository(MlbTotalsSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: MlbTotalsSnapshotRecord) -> bool:
        existing = (
            self.db.query(MlbTeamBetTotalsPregameSnapshot)
            .filter_by(
                observation_time=record.observation_time,
                event_id=record.event_id,
                bookmaker=record.bookmaker,
                outcome_name=record.outcome_name,
                snapshot_version=record.snapshot_version,
            )
            .first()
        )
        if existing is not None:
            return False

        self.db.add(MlbTeamBetTotalsPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
