"""ABC for CFB totals hit-rate reads."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.team_bets.upstream_rows import TeamBetTotalsHitRateRow


class CfbTotalsHitRateReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetTotalsHitRateRow]:
        """Return ``cfb_team_bet_totals_hit_rates`` rows observable at ``observation_time``."""
