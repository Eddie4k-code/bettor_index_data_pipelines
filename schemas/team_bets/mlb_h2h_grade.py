"""MLB moneyline post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class MlbH2hGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "baseball_mlb"
    market_key: str = "h2h"
    grade_version: str = "mlb_h2h_grade_v1"
