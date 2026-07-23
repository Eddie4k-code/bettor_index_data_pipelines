"""NBA totals post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class NbaTotalsGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "basketball_nba"
    market_key: str = "totals"
    grade_version: str = "nba_totals_grade_v1"
