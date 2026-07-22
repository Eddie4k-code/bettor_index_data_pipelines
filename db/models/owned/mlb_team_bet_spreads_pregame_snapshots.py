"""Owned MLB team bet spreads pregame snapshot table."""

from db.models.base import Base
from db.models.owned.mixins import TeamBetSnapshotBaseColumns, TeamBetSpreadsFeatureColumns


class MlbTeamBetSpreadsPregameSnapshot(
    TeamBetSnapshotBaseColumns,
    TeamBetSpreadsFeatureColumns,
    Base,
):
    __tablename__ = "mlb_team_bet_spreads_pregame_snapshots"
