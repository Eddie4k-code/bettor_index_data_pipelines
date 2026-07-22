"""NBA moneyline pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.h2h_features import TeamBetH2hFeatures


class NbaH2hSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetH2hFeatures):
    sport_key: str = "basketball_nba"
    market_key: str = "h2h"
    snapshot_version: str = "nba_h2h_v1"
