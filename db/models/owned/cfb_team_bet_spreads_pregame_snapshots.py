"""Owned CFB team bet spreads pregame snapshot table."""

from db.models.base import Base
from db.models.owned.mixins import TeamBetSnapshotBaseColumns, TeamBetSpreadsFeatureColumns


class CfbTeamBetSpreadsPregameSnapshot(
    TeamBetSnapshotBaseColumns,
    TeamBetSpreadsFeatureColumns,
    Base,
):
    __tablename__ = "cfb_team_bet_spreads_pregame_snapshots"
