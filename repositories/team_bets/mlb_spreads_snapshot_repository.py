"""Append-only writes to ``mlb_team_bet_spreads_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.mlb_team_bet_spreads_pregame_snapshots import MlbTeamBetSpreadsPregameSnapshot
from interfaces.mlb_spreads_snapshot_repository_interface import MlbSpreadsSnapshotRepositoryInterface
from schemas.team_bets import MlbSpreadsSnapshotRecord


class MlbSpreadsSnapshotRepository(MlbSpreadsSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: MlbSpreadsSnapshotRecord) -> bool:
        existing = (
            self.db.query(MlbTeamBetSpreadsPregameSnapshot)
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

        self.db.add(MlbTeamBetSpreadsPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
