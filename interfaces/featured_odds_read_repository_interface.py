"""ABC for point-in-time featured odds reads."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.team_bets.upstream_rows import FeaturedOddsRow


class FeaturedOddsReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_pregame_odds(
        self,
        *,
        sport_key: str,
        market_key: str,
        observation_time: datetime,
    ) -> list[FeaturedOddsRow]:
        """Return featured odds rows observable at ``observation_time``."""
