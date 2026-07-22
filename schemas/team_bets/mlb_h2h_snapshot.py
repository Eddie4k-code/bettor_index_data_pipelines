"""MLB moneyline pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.h2h_features import TeamBetH2hFeatures


class MlbH2hSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetH2hFeatures):
    sport_key: str = "baseball_mlb"
    market_key: str = "h2h"
    snapshot_version: str = "mlb_h2h_v1"
