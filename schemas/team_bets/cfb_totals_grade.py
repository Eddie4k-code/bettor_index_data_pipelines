"""CFB totals post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class CfbTotalsGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "americanfootball_ncaaf"
    market_key: str = "totals"
    grade_version: str = "cfb_totals_grade_v1"
