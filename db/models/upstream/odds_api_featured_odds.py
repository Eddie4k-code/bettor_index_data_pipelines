"""Read-only mirror of revised_engine ``odds_api_featured_odds``."""

import datetime

from sqlalchemy import Column, DateTime, Float, String

from db.models.base import UpstreamBase


class OddsAPIFeaturedOdds(UpstreamBase):
    __tablename__ = "odds_api_featured_odds"

    event_id = Column(String, primary_key=True)
    bookmaker = Column(String, primary_key=True)
    market_key = Column(String, primary_key=True)
    outcome_name = Column(String, primary_key=True)
    outcome_price = Column(Float, nullable=False)
    outcome_point = Column(Float)
    commence_time = Column(DateTime)
    sport_key = Column(String, nullable=False, index=True)
    sport_title = Column(String, nullable=True)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    market_last_update = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
