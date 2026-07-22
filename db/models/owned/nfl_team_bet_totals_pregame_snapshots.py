"""Owned NFL team bet totals pregame snapshot table."""

from db.models.base import Base
from db.models.owned.mixins import TeamBetSnapshotBaseColumns, TeamBetTotalsFeatureColumns


class NflTeamBetTotalsPregameSnapshot(
    TeamBetSnapshotBaseColumns,
    TeamBetTotalsFeatureColumns,
    Base,
):
    __tablename__ = "nfl_team_bet_totals_pregame_snapshots"
