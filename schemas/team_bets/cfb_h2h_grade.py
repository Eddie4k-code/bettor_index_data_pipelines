"""CFB moneyline post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class CfbH2hGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "americanfootball_ncaaf"
    market_key: str = "h2h"
    grade_version: str = "cfb_h2h_grade_v1"
