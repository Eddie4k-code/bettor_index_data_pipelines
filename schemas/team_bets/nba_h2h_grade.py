"""NBA moneyline post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class NbaH2hGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "basketball_nba"
    market_key: str = "h2h"
    grade_version: str = "nba_h2h_grade_v1"
