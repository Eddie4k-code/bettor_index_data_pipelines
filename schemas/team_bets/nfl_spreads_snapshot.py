"""NFL spread pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.spreads_features import TeamBetSpreadsFeatures


class NflSpreadsSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetSpreadsFeatures):
    sport_key: str = "americanfootball_nfl"
    market_key: str = "spreads"
    snapshot_version: str = "nfl_spreads_v1"
