"""Stub hit-rate reads for CFB H2H until upstream tables exist."""

from datetime import datetime

from interfaces.cfb_h2h_hit_rate_read_repository_interface import CfbH2hHitRateReadRepositoryInterface
from schemas.team_bets.upstream_rows import TeamBetH2hHitRateRow


class CfbH2hHitRateReadRepository(CfbH2hHitRateReadRepositoryInterface):
    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetH2hHitRateRow]:
        return []
