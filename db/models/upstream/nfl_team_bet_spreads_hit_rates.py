"""Read-only mirror of hit_rate_worker ``nfl_team_bet_spreads_hit_rates``."""

from sqlalchemy import Column, Float, Integer, String, Text

from db.models.base import UpstreamBase


class NflTeamBetSpreadsHitRates(UpstreamBase):
    __tablename__ = "nfl_team_bet_spreads_hit_rates"

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
    outcome_team_id = Column(Integer, nullable=True)
    market_last_update = Column(String, nullable=False)
    sport_key = Column(String, nullable=False, index=True)
    spread = Column(Float, nullable=False)
    last_n_covers = Column(Integer, nullable=False)
    last_n_sample = Column(Integer, nullable=False)
    last_n_window = Column(Integer, nullable=False)
    last_n_margins = Column(Text, nullable=True)
    h2h_covers = Column(Integer, nullable=False)
    h2h_sample = Column(Integer, nullable=False)
    h2h_window = Column(Integer, nullable=False)
    h2h_margins = Column(Text, nullable=True)
    venue_covers = Column(Integer, nullable=False)
    venue_sample = Column(Integer, nullable=False)
    venue_window = Column(Integer, nullable=False)
    venue_type = Column(String, nullable=False)
    venue_margins = Column(Text, nullable=True)
