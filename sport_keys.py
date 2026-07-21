"""Sport key normalization."""

from typing import Final

SPORT_KEY_ALIASES: Final[dict[str, str]] = {
    "football_nfl": "americanfootball_nfl",
    "americanfootball_nfl": "americanfootball_nfl",
    "basketball_nba": "basketball_nba",
    "baseball_mlb": "baseball_mlb",
}

SUPPORTED_SPORT_KEYS: Final[frozenset[str]] = frozenset({
    "basketball_nba",
    "baseball_mlb",
    "americanfootball_nfl",
})


def normalize_sport_key(sport: str) -> str:
    """Normalize any supported sport alias to the canonical sport key."""
    normalized = sport.strip().lower()
    return SPORT_KEY_ALIASES.get(normalized, normalized)
