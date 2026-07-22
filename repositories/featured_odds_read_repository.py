"""Point-in-time reads from ``odds_api_featured_odds``."""

from datetime import datetime

from sqlalchemy.orm import Session

from db.models.upstream.odds_api_featured_odds import OddsAPIFeaturedOdds
from interfaces.featured_odds_read_repository_interface import FeaturedOddsReadRepositoryInterface
from schemas.snapshot import ALLOWED_BOOKMAKERS
from schemas.team_bets.upstream_rows import FeaturedOddsRow


class FeaturedOddsReadRepository(FeaturedOddsReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_pregame_odds(
        self,
        *,
        sport_key: str,
        market_key: str,
        observation_time: datetime,
    ) -> list[FeaturedOddsRow]:
        rows = (
            self.db.query(OddsAPIFeaturedOdds)
            .filter(
                OddsAPIFeaturedOdds.sport_key == sport_key,
                OddsAPIFeaturedOdds.market_key == market_key,
                OddsAPIFeaturedOdds.market_last_update <= observation_time,
                OddsAPIFeaturedOdds.commence_time > observation_time,
                OddsAPIFeaturedOdds.bookmaker.in_(ALLOWED_BOOKMAKERS),
            )
            .all()
        )
        return [self._to_row(row) for row in rows]

    @staticmethod
    def _to_row(row: OddsAPIFeaturedOdds) -> FeaturedOddsRow:
        return FeaturedOddsRow(
            event_id=row.event_id,
            bookmaker=row.bookmaker,
            market_key=row.market_key,
            outcome_name=row.outcome_name,
            sport_key=row.sport_key,
            commence_time=row.commence_time,
            outcome_price=row.outcome_price,
            outcome_point=row.outcome_point,
            market_last_update=row.market_last_update,
            home_team=row.home_team,
            away_team=row.away_team,
        )
