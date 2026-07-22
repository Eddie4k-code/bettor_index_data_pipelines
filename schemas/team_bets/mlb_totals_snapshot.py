"""MLB totals pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.totals_features import TeamBetTotalsFeatures


class MlbTotalsSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetTotalsFeatures):
    sport_key: str = "baseball_mlb"
    market_key: str = "totals"
    snapshot_version: str = "mlb_totals_v1"
