"""Owned NBA team bet spreads pregame snapshot table."""

from sqlalchemy import Column, DateTime, Float, Integer, String

from db.models.base import Base


class NbaTeamBetSpreadsPregameSnapshot(Base):
    __tablename__ = "nba_team_bet_spreads_pregame_snapshots"

    observation_time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    event_id = Column(String, primary_key=True, nullable=False)
    bookmaker = Column(String, primary_key=True, nullable=False)
    outcome_name = Column(String, primary_key=True, nullable=False)
    snapshot_version = Column(String, primary_key=True, nullable=False)
    sport_key = Column(String, nullable=False, index=True)
    market_key = Column(String, nullable=False, index=True)
    commence_time = Column(DateTime(timezone=True), nullable=False)
    outcome_point = Column(Float, nullable=True)
    outcome_price = Column(Float, nullable=False)
    market_last_update = Column(DateTime(timezone=True), nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_team_id = Column(Integer, nullable=True)
    away_team_id = Column(Integer, nullable=True)
    outcome_team_id = Column(Integer, nullable=True)
    hit_rate_market_last_update = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    season = Column(Integer, nullable=True)
    spread = Column(Float, nullable=False)
    last_n_covers = Column(Integer, nullable=False)
    last_n_sample = Column(Integer, nullable=False)
    last_n_window = Column(Integer, nullable=False)
    h2h_covers = Column(Integer, nullable=False)
    h2h_sample = Column(Integer, nullable=False)
    h2h_window = Column(Integer, nullable=False)
    venue_covers = Column(Integer, nullable=False)
    venue_sample = Column(Integer, nullable=False)
    venue_window = Column(Integer, nullable=False)
    venue_type = Column(String, nullable=False)
