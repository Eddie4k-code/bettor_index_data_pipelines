"""Owned MLB team bet h2h pregame snapshot table."""

from db.models.base import Base
from db.models.owned.mixins import TeamBetH2hFeatureColumns, TeamBetSnapshotBaseColumns


class MlbTeamBetH2hPregameSnapshot(TeamBetSnapshotBaseColumns, TeamBetH2hFeatureColumns, Base):
    __tablename__ = "mlb_team_bet_h2h_pregame_snapshots"
