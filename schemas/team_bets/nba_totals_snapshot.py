"""NBA totals pregame snapshot row."""

from schemas.snapshot import TeamBetSnapshotRecordBase
from schemas.team_bets.totals_features import TeamBetTotalsFeatures


class NbaTotalsSnapshotRecord(TeamBetSnapshotRecordBase, TeamBetTotalsFeatures):
    sport_key: str = "basketball_nba"
    market_key: str = "totals"
    snapshot_version: str = "nba_totals_v1"
