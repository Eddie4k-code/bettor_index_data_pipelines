"""Append-only writes to ``cfb_team_bet_spreads_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.cfb_team_bet_spreads_pregame_snapshots import CfbTeamBetSpreadsPregameSnapshot
from interfaces.cfb_spreads_snapshot_repository_interface import CfbSpreadsSnapshotRepositoryInterface
from schemas.team_bets import CfbSpreadsSnapshotRecord


class CfbSpreadsSnapshotRepository(CfbSpreadsSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: CfbSpreadsSnapshotRecord) -> bool:
        existing = (
            self.db.query(CfbTeamBetSpreadsPregameSnapshot)
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

        self.db.add(CfbTeamBetSpreadsPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
