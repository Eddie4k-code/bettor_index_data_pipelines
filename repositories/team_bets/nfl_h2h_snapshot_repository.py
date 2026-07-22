"""Append-only writes to ``nfl_team_bet_h2h_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.nfl_team_bet_h2h_pregame_snapshots import NflTeamBetH2hPregameSnapshot
from interfaces.nfl_h2h_snapshot_repository_interface import NflH2hSnapshotRepositoryInterface
from schemas.team_bets import NflH2hSnapshotRecord


class NflH2hSnapshotRepository(NflH2hSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NflH2hSnapshotRecord) -> bool:
        existing = (
            self.db.query(NflTeamBetH2hPregameSnapshot)
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

        self.db.add(NflTeamBetH2hPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
