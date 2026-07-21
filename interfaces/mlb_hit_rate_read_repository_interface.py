"""Contract for read-only lookups against ``mlb_hit_rates``."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.mlb_hit_rate import MLBHitRateRow


class MLBHitRateReadRepositoryInterface(ABC):
    """Fetches hit-rate feature rows for snapshot assembly."""

    @abstractmethod
    def fetch_hit_rate(
        self,
        *,
        event_id: str,
        bookmaker: str,
        market_key: str,
        outcome_description: str | None,
        outcome_name: str,
        outcome_point: float,
        observation_time: datetime,
    ) -> MLBHitRateRow | None:
        """Return the hit-rate row when present and market_last_update <= observation_time."""
        pass
