"""Point-in-time reads from ``nfl_team_bet_hit_rates``."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.upstream.nfl_team_bet_hit_rates import NflTeamBetHitRates
from interfaces.nfl_h2h_hit_rate_read_repository_interface import NflH2hHitRateReadRepositoryInterface
from repositories.team_bets._upstream_hit_rate_reads import (
    is_observable_at_observation_time,
    map_h2h_hit_rate_row,
)
from schemas.snapshot import ALLOWED_BOOKMAKERS
from schemas.team_bets.upstream_rows import TeamBetH2hHitRateRow


class NflH2hHitRateReadRepository(NflH2hHitRateReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetH2hHitRateRow]:
        rows = (
            self.db.query(NflTeamBetHitRates)
            .filter(
                NflTeamBetHitRates.market_key == "h2h",
                NflTeamBetHitRates.bookmaker.in_(ALLOWED_BOOKMAKERS),
            )
            .all()
        )
        return [
            dto
            for row in rows
            if (dto := map_h2h_hit_rate_row(row)) is not None
            and is_observable_at_observation_time(row, observation_time)
        ]
