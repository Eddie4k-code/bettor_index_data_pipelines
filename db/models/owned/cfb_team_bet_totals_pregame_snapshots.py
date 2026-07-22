"""Owned CFB team bet totals pregame snapshot table."""

from db.models.base import Base
from db.models.owned.mixins import TeamBetSnapshotBaseColumns, TeamBetTotalsFeatureColumns


class CfbTeamBetTotalsPregameSnapshot(
    TeamBetSnapshotBaseColumns,
    TeamBetTotalsFeatureColumns,
    Base,
):
    __tablename__ = "cfb_team_bet_totals_pregame_snapshots"
