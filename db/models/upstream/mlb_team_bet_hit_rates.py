"""Read-only mirror of hit_rate_worker ``mlb_team_bet_hit_rates``."""

from sqlalchemy import Column, Integer, String

from db.models.base import UpstreamBase


class MlbTeamBetHitRates(UpstreamBase):
    __tablename__ = "mlb_team_bet_hit_rates"

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
    last_n_wins = Column(Integer, nullable=True)
    last_n_losses = Column(Integer, nullable=True)
    last_n_sample = Column(Integer, nullable=True)
    last_n_window = Column(Integer, nullable=True)
    venue_wins = Column(Integer, nullable=True)
    venue_losses = Column(Integer, nullable=True)
    venue_sample = Column(Integer, nullable=True)
    venue_window = Column(Integer, nullable=True)
    venue_type = Column(String, nullable=True)
    h2h_wins = Column(Integer, nullable=True)
    h2h_losses = Column(Integer, nullable=True)
    h2h_sample = Column(Integer, nullable=True)
    h2h_window = Column(Integer, nullable=True)
