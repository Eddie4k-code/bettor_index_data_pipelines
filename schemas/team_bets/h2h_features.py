"""W/L window fields copied from upstream {sport}_team_bet_hit_rates rows."""

from pydantic import BaseModel, ConfigDict


class TeamBetH2hFeatures(BaseModel):
    """Moneyline hit-rate features shared across NBA, MLB, NFL, and CFB snapshots."""

    model_config = ConfigDict(from_attributes=True, frozen=True, extra="forbid")

    last_n_wins: int | None = None
    last_n_losses: int | None = None
    last_n_sample: int | None = None
    last_n_window: int | None = None
    venue_wins: int | None = None
    venue_losses: int | None = None
    venue_sample: int | None = None
    venue_window: int | None = None
    venue_type: str | None = None
    h2h_wins: int | None = None
    h2h_losses: int | None = None
    h2h_sample: int | None = None
    h2h_window: int | None = None
