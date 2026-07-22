"""Read-only mirror of hit_rate_worker ``nfl_team_bet_totals_hit_rates``."""

from sqlalchemy import Column, Float, Integer, String, Text

from db.models.base import UpstreamBase


class NflTeamBetTotalsHitRates(UpstreamBase):
    __tablename__ = "nfl_team_bet_totals_hit_rates"

    event_id = Column(String, primary_key=True, nullable=False)
    bookmaker = Column(String, primary_key=True, nullable=False)
    market_key = Column(String, primary_key=True, nullable=False)
    outcome_name = Column(String, primary_key=True, nullable=False)
    commence_time = Column(String, nullable=False)
    outcome_price = Column(String, nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_team_id = Column(Integer, nullable=True)
    away_team_id = Column(Integer, nullable=True)
    market_last_update = Column(String, nullable=False)
    sport_key = Column(String, nullable=False, index=True)
    direction = Column(String, nullable=False)
    line = Column(Float, nullable=False)
    configured_window = Column(Integer, nullable=False)
    home_team_clears = Column(Integer, nullable=False)
    home_team_sample = Column(Integer, nullable=False)
    away_team_clears = Column(Integer, nullable=False)
    away_team_sample = Column(Integer, nullable=False)
    h2h_window = Column(Integer, nullable=False)
    h2h_sample = Column(Integer, nullable=False)
    h2h_combined_totals = Column(Text, nullable=True)
    h2h_clears = Column(Integer, nullable=False)
    h2h_avg_total = Column(Float, nullable=True)
