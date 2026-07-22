"""Append-only writes to ``nfl_team_bet_spreads_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.nfl_team_bet_spreads_pregame_snapshots import NflTeamBetSpreadsPregameSnapshot
from interfaces.nfl_spreads_snapshot_repository_interface import NflSpreadsSnapshotRepositoryInterface
from schemas.team_bets import NflSpreadsSnapshotRecord


class NflSpreadsSnapshotRepository(NflSpreadsSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NflSpreadsSnapshotRecord) -> bool:
        existing = (
            self.db.query(NflTeamBetSpreadsPregameSnapshot)
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

        self.db.add(NflTeamBetSpreadsPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
