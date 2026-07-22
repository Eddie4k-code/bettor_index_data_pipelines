"""Append-only writes to ``nba_team_bet_h2h_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.nba_team_bet_h2h_pregame_snapshots import NbaTeamBetH2hPregameSnapshot
from interfaces.nba_h2h_snapshot_repository_interface import NbaH2hSnapshotRepositoryInterface
from schemas.team_bets import NbaH2hSnapshotRecord


class NbaH2hSnapshotRepository(NbaH2hSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NbaH2hSnapshotRecord) -> bool:
        existing = (
            self.db.query(NbaTeamBetH2hPregameSnapshot)
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

        self.db.add(NbaTeamBetH2hPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
