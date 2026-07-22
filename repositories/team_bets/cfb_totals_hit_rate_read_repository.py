"""Stub hit-rate reads for CFB totals until upstream tables exist."""

from datetime import datetime

from interfaces.cfb_totals_hit_rate_read_repository_interface import CfbTotalsHitRateReadRepositoryInterface
from schemas.team_bets.upstream_rows import TeamBetTotalsHitRateRow


class CfbTotalsHitRateReadRepository(CfbTotalsHitRateReadRepositoryInterface):
    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetTotalsHitRateRow]:
        return []
