"""Point-in-time reads from ``nfl_team_bet_spreads_hit_rates``."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.upstream.nfl_team_bet_spreads_hit_rates import NflTeamBetSpreadsHitRates
from interfaces.nfl_spreads_hit_rate_read_repository_interface import NflSpreadsHitRateReadRepositoryInterface
from repositories.team_bets._upstream_hit_rate_reads import (
    is_observable_at_observation_time,
    map_spreads_hit_rate_row,
)
from schemas.snapshot import ALLOWED_BOOKMAKERS
from schemas.team_bets.upstream_rows import TeamBetSpreadsHitRateRow


class NflSpreadsHitRateReadRepository(NflSpreadsHitRateReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetSpreadsHitRateRow]:
        rows = (
            self.db.query(NflTeamBetSpreadsHitRates)
            .filter(
                NflTeamBetSpreadsHitRates.market_key == "spreads",
                NflTeamBetSpreadsHitRates.bookmaker.in_(ALLOWED_BOOKMAKERS),
            )
            .all()
        )
        return [
            dto
            for row in rows
            if (dto := map_spreads_hit_rate_row(row)) is not None
            and is_observable_at_observation_time(row, observation_time)
        ]
