"""Cover window fields copied from upstream {sport}_team_bet_spreads_hit_rates rows."""

from pydantic import BaseModel, ConfigDict


class TeamBetSpreadsFeatures(BaseModel):
    """Spread cover features shared across NBA, MLB, NFL, and CFB snapshots."""

    model_config = ConfigDict(from_attributes=True, frozen=True, extra="forbid")

    spread: float
    last_n_covers: int
    last_n_sample: int
    last_n_window: int
    h2h_covers: int
    h2h_sample: int
    h2h_window: int
    venue_covers: int
    venue_sample: int
    venue_window: int
    venue_type: str
