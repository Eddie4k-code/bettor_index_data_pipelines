"""Tests for team-bet snapshot feature mixins (h2h, spreads, totals)."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from schemas.team_bets import (
    NbaH2hSnapshotRecord,
    NbaSpreadsSnapshotRecord,
    NbaTotalsSnapshotRecord,
    TeamBetH2hFeatures,
    TeamBetSpreadsFeatures,
    TeamBetTotalsFeatures,
)


def _base_record_kwargs(**overrides):
    defaults = {
        "observation_time": datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc),
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "commence_time": datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc),
        "outcome_point": None,
        "outcome_price": -110.0,
        "market_last_update": datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "outcome_team_id": 1,
        "hit_rate_market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "created_at": datetime(2026, 7, 21, 12, 5, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return defaults


def _h2h_feature_kwargs(**overrides):
    defaults = {
        "last_n_wins": 7,
        "last_n_losses": 3,
        "last_n_sample": 10,
        "last_n_window": 10,
        "venue_wins": 4,
        "venue_losses": 1,
        "venue_sample": 5,
        "venue_window": 10,
        "venue_type": "home",
        "h2h_wins": 2,
        "h2h_losses": 1,
        "h2h_sample": 3,
        "h2h_window": 10,
    }
    defaults.update(overrides)
    return defaults


def _spreads_feature_kwargs(**overrides):
    defaults = {
        "spread": -3.5,
        "last_n_covers": 6,
        "last_n_sample": 10,
        "last_n_window": 10,
        "h2h_covers": 2,
        "h2h_sample": 3,
        "h2h_window": 10,
        "venue_covers": 4,
        "venue_sample": 5,
        "venue_window": 10,
        "venue_type": "home",
    }
    defaults.update(overrides)
    return defaults


def _totals_feature_kwargs(**overrides):
    defaults = {
        "direction": "over",
        "line": 224.5,
        "configured_window": 10,
        "home_team_clears": 6,
        "home_team_sample": 10,
        "away_team_clears": 5,
        "away_team_sample": 10,
        "h2h_window": 10,
        "h2h_sample": 3,
        "h2h_clears": 2,
        "h2h_avg_total": 218.3,
    }
    defaults.update(overrides)
    return defaults


def test_h2h_features_accepts_window_fields():
    features = TeamBetH2hFeatures(**_h2h_feature_kwargs())

    assert features.last_n_wins == 7
    assert features.venue_type == "home"
    assert features.h2h_sample == 3


def test_h2h_features_allow_null_window_counts():
    features = TeamBetH2hFeatures(**_h2h_feature_kwargs(last_n_wins=None, h2h_losses=None))

    assert features.last_n_wins is None
    assert features.h2h_losses is None


def test_h2h_record_composes_base_and_features():
    record = NbaH2hSnapshotRecord(**_base_record_kwargs(), **_h2h_feature_kwargs())

    assert record.market_key == "h2h"
    assert record.snapshot_version == "nba_h2h_v1"
    assert record.last_n_wins == 7


def test_spreads_features_accepts_cover_windows():
    features = TeamBetSpreadsFeatures(**_spreads_feature_kwargs())

    assert features.spread == -3.5
    assert features.venue_covers == 4


def test_spreads_features_reject_margin_blobs():
    with pytest.raises(ValidationError):
        TeamBetSpreadsFeatures(**_spreads_feature_kwargs(last_n_margins="[-3,1,7]"))


def test_spreads_record_composes_base_and_features():
    record = NbaSpreadsSnapshotRecord(
        **_base_record_kwargs(outcome_point=-3.5),
        **_spreads_feature_kwargs(),
    )

    assert record.market_key == "spreads"
    assert record.spread == -3.5
    assert record.last_n_covers == 6


def test_totals_features_accepts_clear_windows():
    features = TeamBetTotalsFeatures(**_totals_feature_kwargs(h2h_avg_total=None))

    assert features.direction == "over"
    assert features.h2h_avg_total is None


def test_totals_features_reject_combined_totals_blob():
    with pytest.raises(ValidationError):
        TeamBetTotalsFeatures(**_totals_feature_kwargs(h2h_combined_totals="[210,225,198]"))


def test_totals_record_composes_base_and_features():
    record = NbaTotalsSnapshotRecord(
        **_base_record_kwargs(
            outcome_name="over",
            outcome_point=224.5,
            outcome_team_id=None,
        ),
        **_totals_feature_kwargs(),
    )

    assert record.market_key == "totals"
    assert record.line == 224.5
    assert record.home_team_clears == 6
