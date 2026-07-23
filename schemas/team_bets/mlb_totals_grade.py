"""MLB totals post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class MlbTotalsGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "baseball_mlb"
    market_key: str = "totals"
    grade_version: str = "mlb_totals_grade_v1"
