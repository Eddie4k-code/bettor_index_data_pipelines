"""CFB spread pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.spreads_features import TeamBetSpreadsFeatures


class CfbSpreadsSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetSpreadsFeatures):
    sport_key: str = "americanfootball_ncaaf"
    market_key: str = "spreads"
    snapshot_version: str = "cfb_spreads_v1"
