"""CFB moneyline pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.h2h_features import TeamBetH2hFeatures


class CfbH2hSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetH2hFeatures):
    sport_key: str = "americanfootball_ncaaf"
    market_key: str = "h2h"
    snapshot_version: str = "cfb_h2h_v1"
