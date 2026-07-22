"""Stub hit-rate reads for CFB spreads until upstream tables exist."""

from datetime import datetime

from interfaces.cfb_spreads_hit_rate_read_repository_interface import CfbSpreadsHitRateReadRepositoryInterface
from schemas.team_bets.upstream_rows import TeamBetSpreadsHitRateRow


class CfbSpreadsHitRateReadRepository(CfbSpreadsHitRateReadRepositoryInterface):
    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetSpreadsHitRateRow]:
        return []
