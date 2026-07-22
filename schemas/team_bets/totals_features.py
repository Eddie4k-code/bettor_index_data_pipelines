"""Clear window fields copied from upstream {sport}_team_bet_totals_hit_rates rows."""

from pydantic import BaseModel, ConfigDict


class TeamBetTotalsFeatures(BaseModel):
    """Totals clear features shared across NBA, MLB, NFL, and CFB snapshots."""

    model_config = ConfigDict(from_attributes=True, frozen=True, extra="forbid")

    direction: str
    line: float
    configured_window: int
    home_team_clears: int
    home_team_sample: int
    away_team_clears: int
    away_team_sample: int
    h2h_window: int
    h2h_sample: int
    h2h_clears: int
    h2h_avg_total: float | None = None
