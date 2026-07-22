"""NFL totals pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.totals_features import TeamBetTotalsFeatures


class NflTotalsSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetTotalsFeatures):
    sport_key: str = "americanfootball_nfl"
    market_key: str = "totals"
    snapshot_version: str = "nfl_totals_v1"
