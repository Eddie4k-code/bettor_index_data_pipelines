"""Append-only writes to ``cfb_team_bet_totals_pregame_snapshots``."""

from sqlalchemy.orm import Session

from db.models.owned.cfb_team_bet_totals_pregame_snapshots import CfbTeamBetTotalsPregameSnapshot
from interfaces.cfb_totals_snapshot_repository_interface import CfbTotalsSnapshotRepositoryInterface
from schemas.team_bets import CfbTotalsSnapshotRecord


class CfbTotalsSnapshotRepository(CfbTotalsSnapshotRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def insert_if_absent(self, record: CfbTotalsSnapshotRecord) -> bool:
        existing = (
            self.db.query(CfbTeamBetTotalsPregameSnapshot)
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

        self.db.add(CfbTeamBetTotalsPregameSnapshot(**record.model_dump()))
        self.db.commit()
        return True
