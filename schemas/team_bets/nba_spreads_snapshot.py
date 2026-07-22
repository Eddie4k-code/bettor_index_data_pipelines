"""NBA spread pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.spreads_features import TeamBetSpreadsFeatures


class NbaSpreadsSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetSpreadsFeatures):
    sport_key: str = "basketball_nba"
    market_key: str = "spreads"
    snapshot_version: str = "nba_spreads_v1"
