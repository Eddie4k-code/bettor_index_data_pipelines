"""CFB spread post-game grade row."""

from schemas.grade import TeamBetGradeRecordBase


class CfbSpreadsGradeRecord(TeamBetGradeRecordBase):
    sport_key: str = "americanfootball_ncaaf"
    market_key: str = "spreads"
    grade_version: str = "cfb_spreads_grade_v1"
