"""ABC for MLB H2H hit-rate reads."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.team_bets.upstream_rows import TeamBetH2hHitRateRow


class MlbH2hHitRateReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetH2hHitRateRow]:
        """Return ``mlb_team_bet_hit_rates`` rows observable at ``observation_time``."""
