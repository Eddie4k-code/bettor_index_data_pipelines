"""Append-only writes to ``nba_team_bet_spreads_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.nba_team_bet_spreads_pregame_snapshots import NbaTeamBetSpreadsPregameSnapshot
from interfaces.nba_spreads_snapshot_repository_interface import NbaSpreadsSnapshotRepositoryInterface
from schemas.team_bets import NbaSpreadsSnapshotRecord


class NbaSpreadsSnapshotRepository(NbaSpreadsSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NbaSpreadsSnapshotRecord) -> bool:
        existing = (
            self.db.query(NbaTeamBetSpreadsPregameSnapshot)
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

        self.db.add(NbaTeamBetSpreadsPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
