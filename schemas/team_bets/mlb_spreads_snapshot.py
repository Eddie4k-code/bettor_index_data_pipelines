"""MLB spread pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.spreads_features import TeamBetSpreadsFeatures


class MlbSpreadsSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetSpreadsFeatures):
    sport_key: str = "baseball_mlb"
    market_key: str = "spreads"
    snapshot_version: str = "mlb_spreads_v1"
