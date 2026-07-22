"""Tests for the NBA H2H team-bet snapshot vertical slice (pipeline + mocked repos)."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from builders.team_bets.h2h_snapshot_builder import H2hSnapshotBuilder
from pipelines.team_bets.nba_h2h_snapshot_pipeline import NbaH2hSnapshotPipeline
from schemas.snapshot import SnapshotRequest, SnapshotRunResult
from schemas.team_bets import NbaH2hSnapshotRecord
from schemas.team_bets.upstream_rows import FeaturedOddsRow, TeamBetH2hHitRateRow

OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)
CREATED_AT = datetime(2026, 7, 21, 12, 5, tzinfo=timezone.utc)
COMMENCE_TIME = datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc)


def _request(**overrides) -> SnapshotRequest:
    defaults = {
        "sport_key": "basketball_nba",
        "market_key": "h2h",
        "observation_time": OBSERVATION_TIME,
    }
    defaults.update(overrides)
    return SnapshotRequest(**defaults)


def _odds_row(**overrides) -> FeaturedOddsRow:
    defaults = {
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "market_key": "h2h",
        "outcome_name": "Boston Celtics",
        "sport_key": "basketball_nba",
        "commence_time": COMMENCE_TIME,
        "outcome_price": -110.0,
        "outcome_point": None,
        "market_last_update": datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
    }
    defaults.update(overrides)
    return FeaturedOddsRow(**defaults)


def _hit_rate_row(**overrides) -> TeamBetH2hHitRateRow:
    defaults = {
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "market_key": "h2h",
        "outcome_name": "Boston Celtics",
        "market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "outcome_team_id": 1,
        "last_n_wins": 7,
        "last_n_losses": 3,
        "last_n_sample": 10,
        "last_n_window": 10,
    }
    defaults.update(overrides)
    return TeamBetH2hHitRateRow(**defaults)


def _pipeline(
    *,
    odds_rows=None,
    hit_rate_rows=None,
    insert_returns=None,
    now_fn=None,
) -> NbaH2hSnapshotPipeline:
    odds_repo = MagicMock()
    odds_repo.fetch_pregame_odds.return_value = odds_rows if odds_rows is not None else []

    hit_rate_repo = MagicMock()
    hit_rate_repo.fetch_pregame_hit_rates.return_value = (
        hit_rate_rows if hit_rate_rows is not None else []
    )

    snapshot_repo = MagicMock()
    if insert_returns is None:
        snapshot_repo.insert_if_absent.return_value = True
    else:
        snapshot_repo.insert_if_absent.side_effect = insert_returns

    return NbaH2hSnapshotPipeline(
        odds_repo=odds_repo,
        hit_rate_repo=hit_rate_repo,
        snapshot_repo=snapshot_repo,
        builder=H2hSnapshotBuilder(),
        now_fn=now_fn or (lambda: CREATED_AT),
    )


class TestNbaH2hSnapshotPipeline:
    def test_snapshots_matching_odds_and_hit_rate_pair(self):
        pipeline = _pipeline(
            odds_rows=[_odds_row()],
            hit_rate_rows=[_hit_rate_row()],
        )

        result = pipeline.run(_request())

        assert result == SnapshotRunResult(
            candidates=1,
            snapshotted=1,
            skipped_existing=0,
            skipped_leakage=0,
        )
        pipeline.snapshot_repo.insert_if_absent.assert_called_once()
        record = pipeline.snapshot_repo.insert_if_absent.call_args.args[0]
        assert isinstance(record, NbaH2hSnapshotRecord)
        assert record.snapshot_version == "nba_h2h_v1"

    def test_skips_existing_snapshot_rows(self):
        pipeline = _pipeline(
            odds_rows=[_odds_row()],
            hit_rate_rows=[_hit_rate_row()],
            insert_returns=[False],
        )

        result = pipeline.run(_request())

        assert result.snapshotted == 0
        assert result.skipped_existing == 1

    def test_skips_leakage_when_builder_rejects_pair(self):
        pipeline = _pipeline(
            odds_rows=[
                _odds_row(
                    market_last_update=datetime(2026, 7, 21, 12, 1, tzinfo=timezone.utc),
                ),
            ],
            hit_rate_rows=[_hit_rate_row()],
        )

        result = pipeline.run(_request())

        assert result.snapshotted == 0
        assert result.skipped_leakage == 1
        pipeline.snapshot_repo.insert_if_absent.assert_not_called()

    def test_skips_when_no_matching_hit_rate_row(self):
        pipeline = _pipeline(
            odds_rows=[_odds_row()],
            hit_rate_rows=[_hit_rate_row(event_id="evt-other")],
        )

        result = pipeline.run(_request())

        assert result.skipped_leakage == 1
        pipeline.snapshot_repo.insert_if_absent.assert_not_called()

    def test_passes_fixed_sport_and_market_to_odds_repo(self):
        pipeline = _pipeline()

        pipeline.run(_request())

        pipeline.odds_repo.fetch_pregame_odds.assert_called_once_with(
            sport_key="basketball_nba",
            market_key="h2h",
            observation_time=OBSERVATION_TIME,
        )

    def test_passes_observation_time_to_hit_rate_repo(self):
        pipeline = _pipeline()

        pipeline.run(_request())

        pipeline.hit_rate_repo.fetch_pregame_hit_rates.assert_called_once_with(
            observation_time=OBSERVATION_TIME,
        )

    @pytest.mark.parametrize(
        "sport_key, market_key",
        [
            ("americanfootball_nfl", "h2h"),
            ("basketball_nba", "spreads"),
        ],
    )
    def test_rejects_mismatched_request(self, sport_key, market_key):
        pipeline = _pipeline()

        with pytest.raises(ValueError, match="basketball_nba.*h2h"):
            pipeline.run(
                _request(sport_key=sport_key, market_key=market_key),
            )
