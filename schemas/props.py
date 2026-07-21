"""Read-model shape for pregame odds rows from ``odds_api_props``."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OddsPropCandidate(BaseModel):
    """One odds row eligible for snapshot assembly at ``observation_time``."""

    model_config = ConfigDict(from_attributes=True, frozen=True)

    event_id: str
    bookmaker: str
    market_key: str
    outcome_name: str
    outcome_description: str
    outcome_point: float | None
    commence_time: datetime
    sport_key: str
    home_team: str
    away_team: str
    market_last_update: datetime
    outcome_price: float
    player_id: int | None = None
