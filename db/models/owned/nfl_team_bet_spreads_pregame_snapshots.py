"""Owned NFL team bet spreads pregame snapshot table."""

from db.models.base import Base
from db.models.owned.mixins import TeamBetSnapshotBaseColumns, TeamBetSpreadsFeatureColumns


class NflTeamBetSpreadsPregameSnapshot(
    TeamBetSnapshotBaseColumns,
    TeamBetSpreadsFeatureColumns,
    Base,
):
    __tablename__ = "nfl_team_bet_spreads_pregame_snapshots"
