"""CFB totals pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.totals_features import TeamBetTotalsFeatures


class CfbTotalsSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetTotalsFeatures):
    sport_key: str = "americanfootball_ncaaf"
    market_key: str = "totals"
    snapshot_version: str = "cfb_totals_v1"
