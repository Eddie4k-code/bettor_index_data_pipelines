"""Tests for canonical sport keys."""

from sport_keys import SUPPORTED_SPORT_KEYS


def test_supported_sport_keys():
    assert SUPPORTED_SPORT_KEYS == frozenset({
        "basketball_nba",
        "baseball_mlb",
        "americanfootball_nfl",
        "americanfootball_ncaaf",
    })
