"""Tests for canonical sport key normalization."""

import pytest

from sport_keys import SUPPORTED_SPORT_KEYS, normalize_sport_key


@pytest.mark.parametrize(
    ("raw", "expected"),
    [
        ("FOOTBALL_NFL", "americanfootball_nfl"),
        ("americanfootball_nfl", "americanfootball_nfl"),
        ("FOOTBALL_NCAAF", "americanfootball_ncaaf"),
        ("americanfootball_ncaaf", "americanfootball_ncaaf"),
        ("basketball_nba", "basketball_nba"),
        ("baseball_mlb", "baseball_mlb"),
    ],
)
def test_normalize_sport_key_maps_aliases_to_canonical_keys(raw, expected):
    assert normalize_sport_key(raw) == expected


def test_supported_sport_keys_includes_cfb():
    assert "americanfootball_ncaaf" in SUPPORTED_SPORT_KEYS
