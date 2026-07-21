"""Read-model shape for rows from ``mlb_hit_rates``."""

from pydantic import BaseModel, ConfigDict


class MLBHitRateRow(BaseModel):
    """Hit-rate features joined onto a pregame odds candidate."""

    model_config = ConfigDict(from_attributes=True, frozen=True)

    event_id: str
    bookmaker: str
    market_key: str
    outcome_description: str | None
    outcome_name: str
    outcome_point: str
    outcome_price: str
    commence_time: str
    sport_key: str
    player_id: int
    season: int | None = None
    ten_game_hit_rate: float | None = None
    thirty_game_hit_rate: float | None = None
    sixty_game_hit_rate: float | None = None
    market_last_update: str
    home_team: str
    away_team: str
    player_team_id: int | None = None
    home_team_id: int | None = None
    away_team_id: int | None = None
