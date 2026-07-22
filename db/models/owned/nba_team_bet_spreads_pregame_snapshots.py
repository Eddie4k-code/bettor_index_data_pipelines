"""Owned NBA team bet spreads pregame snapshot table."""

from db.models.base import Base
from db.models.owned.mixins import TeamBetSnapshotBaseColumns, TeamBetSpreadsFeatureColumns


class NbaTeamBetSpreadsPregameSnapshot(
    TeamBetSnapshotBaseColumns,
    TeamBetSpreadsFeatureColumns,
    Base,
):
    __tablename__ = "nba_team_bet_spreads_pregame_snapshots"
