"""Point-in-time reads from ``nba_team_bet_totals_hit_rates``."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.upstream.nba_team_bet_totals_hit_rates import NbaTeamBetTotalsHitRates
from interfaces.nba_totals_hit_rate_read_repository_interface import NbaTotalsHitRateReadRepositoryInterface
from repositories.team_bets._upstream_hit_rate_reads import (
    is_observable_at_observation_time,
    map_totals_hit_rate_row,
)
from schemas.snapshot import ALLOWED_BOOKMAKERS
from schemas.team_bets.upstream_rows import TeamBetTotalsHitRateRow


class NbaTotalsHitRateReadRepository(NbaTotalsHitRateReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetTotalsHitRateRow]:
        rows = (
            self.db.query(NbaTeamBetTotalsHitRates)
            .filter(
                NbaTeamBetTotalsHitRates.market_key == "totals",
                NbaTeamBetTotalsHitRates.bookmaker.in_(ALLOWED_BOOKMAKERS),
            )
            .all()
        )
        return [
            dto
            for row in rows
            if (dto := map_totals_hit_rate_row(row)) is not None
            and is_observable_at_observation_time(row, observation_time)
        ]
