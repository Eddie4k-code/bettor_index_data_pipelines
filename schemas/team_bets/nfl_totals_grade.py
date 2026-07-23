"""NFL totals post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class NflTotalsGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "americanfootball_nfl"
    market_key: str = "totals"
    grade_version: str = "nfl_totals_grade_v1"
