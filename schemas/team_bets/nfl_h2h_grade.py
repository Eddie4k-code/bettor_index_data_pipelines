"""NFL moneyline post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class NflH2hGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "americanfootball_nfl"
    market_key: str = "h2h"
    grade_version: str = "nfl_h2h_grade_v1"
