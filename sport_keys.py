"""Canonical sport keys for team-bet snapshot pipelines."""

from typing import Final

SUPPORTED_SPORT_KEYS: Final[frozenset[str]] = frozenset({
    "basketball_nba",
    "baseball_mlb",
    "americanfootball_nfl",
    "americanfootball_ncaaf",
})
