"""NBA spread post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class NbaSpreadsGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "basketball_nba"
    market_key: str = "spreads"
    grade_version: str = "nba_spreads_grade_v1"
