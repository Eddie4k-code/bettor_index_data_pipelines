"""ABC for CFB spreads hit-rate reads."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.team_bets.upstream_rows import TeamBetSpreadsHitRateRow


class CfbSpreadsHitRateReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetSpreadsHitRateRow]:
        """Return ``cfb_team_bet_spreads_hit_rates`` rows observable at ``observation_time``."""
