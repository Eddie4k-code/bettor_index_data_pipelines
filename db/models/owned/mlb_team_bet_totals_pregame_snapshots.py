"""Owned MLB team bet totals pregame snapshot table."""

from db.models.base import Base
from db.models.owned.mixins import TeamBetSnapshotBaseColumns, TeamBetTotalsFeatureColumns


class MlbTeamBetTotalsPregameSnapshot(
    TeamBetSnapshotBaseColumns,
    TeamBetTotalsFeatureColumns,
    Base,
):
    __tablename__ = "mlb_team_bet_totals_pregame_snapshots"
