"""NFL spread post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class NflSpreadsGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "americanfootball_nfl"
    market_key: str = "spreads"
    grade_version: str = "nfl_spreads_grade_v1"
