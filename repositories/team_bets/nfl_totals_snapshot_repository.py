"""Append-only writes to ``nfl_team_bet_totals_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.nfl_team_bet_totals_pregame_snapshots import NflTeamBetTotalsPregameSnapshot
from interfaces.nfl_totals_snapshot_repository_interface import NflTotalsSnapshotRepositoryInterface
from schemas.team_bets import NflTotalsSnapshotRecord


class NflTotalsSnapshotRepository(NflTotalsSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: NflTotalsSnapshotRecord) -> bool:
        existing = (
            self.db.query(NflTeamBetTotalsPregameSnapshot)
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

        self.db.add(NflTeamBetTotalsPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
