"""Contract for read-only queries against ``odds_api_props``."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.props import OddsPropCandidate
from schemas.snapshot import ALLOWED_BOOKMAKERS


class PropsReadRepositoryInterface(ABC):
    """Fetches pregame odds rows with temporal filters applied in SQL."""

    @abstractmethod
    def fetch_pregame_props(
        self,
        *,
        sport_key: str,
        market_key: str,
        observation_time: datetime,
        bookmakers: frozenset[str] = ALLOWED_BOOKMAKERS,
    ) -> list[OddsPropCandidate]:
        """Return odds rows where commence_time > observation_time and market_last_update <= observation_time."""
        pass
