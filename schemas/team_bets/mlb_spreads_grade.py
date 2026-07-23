"""MLB spread post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class MlbSpreadsGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "baseball_mlb"
    market_key: str = "spreads"
    grade_version: str = "mlb_spreads_grade_v1"
