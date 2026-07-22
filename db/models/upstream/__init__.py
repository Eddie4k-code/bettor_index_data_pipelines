"""Read-only mirrors of shared PostgreSQL tables (revised_engine / hit_rate_worker)."""

from db.models.upstream.mlb_hit_rates import MLBHitRates
from db.models.upstream.nba_team_bet_hit_rates import NbaTeamBetHitRates
from db.models.upstream.odds_api_featured_odds import OddsAPIFeaturedOdds
from db.models.upstream.odds_api_prop import OddsAPIProp

__all__ = [
    "MLBHitRates",
    "NbaTeamBetHitRates",
    "OddsAPIFeaturedOdds",
    "OddsAPIProp",
]
