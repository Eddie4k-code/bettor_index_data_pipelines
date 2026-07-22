"""ABC for NBA spreads hit-rate reads."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.team_bets.upstream_rows import TeamBetSpreadsHitRateRow


class NbaSpreadsHitRateReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetSpreadsHitRateRow]:
        """Return ``nba_team_bet_spreads_hit_rates`` rows observable at ``observation_time``."""
