"""Append-only writes to ``nba_team_bet_totals_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.nba_team_bet_totals_pregame_snapshots import NbaTeamBetTotalsPregameSnapshot
from interfaces.nba_totals_snapshot_repository_interface import NbaTotalsSnapshotRepositoryInterface
from schemas.team_bets import NbaTotalsSnapshotRecord


class NbaTotalsSnapshotRepository(NbaTotalsSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NbaTotalsSnapshotRecord) -> bool:
        existing = (
            self.db.query(NbaTeamBetTotalsPregameSnapshot)
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

        self.db.add(NbaTeamBetTotalsPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
