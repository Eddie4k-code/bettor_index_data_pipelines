"""Append-only writes to ``cfb_team_bet_h2h_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.cfb_team_bet_h2h_pregame_snapshots import CfbTeamBetH2hPregameSnapshot
from interfaces.cfb_h2h_snapshot_repository_interface import CfbH2hSnapshotRepositoryInterface
from schemas.team_bets import CfbH2hSnapshotRecord


class CfbH2hSnapshotRepository(CfbH2hSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: CfbH2hSnapshotRecord) -> bool:
        existing = (
            self.db.query(CfbTeamBetH2hPregameSnapshot)
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

        self.db.add(CfbTeamBetH2hPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
