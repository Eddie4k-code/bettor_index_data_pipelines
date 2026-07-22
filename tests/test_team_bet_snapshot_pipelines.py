"""Parametrized tests for explicit team-bet snapshot pipelines (11 non-NBA-H2H slices)."""

import importlib
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from builders.team_bets.h2h_snapshot_builder import H2hSnapshotBuilder
from builders.team_bets.spreads_snapshot_builder import SpreadsSnapshotBuilder
from builders.team_bets.totals_snapshot_builder import TotalsSnapshotBuilder
from schemas.snapshot import SnapshotRequest, SnapshotRunResult
from schemas.team_bets.upstream_rows import (
    FeaturedOddsRow,
    TeamBetH2hHitRateRow,
    TeamBetSpreadsHitRateRow,
    TeamBetTotalsHitRateRow,
)

OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)
CREATED_AT = datetime(2026, 7, 21, 12, 5, tzinfo=timezone.utc)
COMMENCE_TIME = datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc)


def _odds_row(*, sport_key: str, market_key: str, **overrides) -> FeaturedOddsRow:
    defaults = {
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "market_key": market_key,
        "outcome_name": "Boston Celtics",
        "sport_key": sport_key,
        "commence_time": COMMENCE_TIME,
        "outcome_price": -110.0,
        "outcome_point": None,
        "market_last_update": datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
    }
    if market_key == "spreads":
        defaults["outcome_point"] = -3.5
    if market_key == "totals":
        defaults["outcome_name"] = "Over"
        defaults["outcome_point"] = 224.5
    defaults.update(overrides)
    return FeaturedOddsRow(**defaults)


def _h2h_hit_rate_row(**overrides) -> TeamBetH2hHitRateRow:
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


def _spreads_hit_rate_row(**overrides) -> TeamBetSpreadsHitRateRow:
    defaults = {
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "market_key": "spreads",
        "outcome_name": "Boston Celtics",
        "market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "outcome_team_id": 1,
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
    return TeamBetSpreadsHitRateRow(**defaults)


def _totals_hit_rate_row(**overrides) -> TeamBetTotalsHitRateRow:
    defaults = {
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "market_key": "totals",
        "outcome_name": "Over",
        "market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "direction": "Over",
        "line": 224.5,
        "configured_window": 10,
        "home_team_clears": 6,
        "home_team_sample": 10,
        "away_team_clears": 5,
        "away_team_sample": 10,
        "h2h_window": 10,
        "h2h_sample": 3,
        "h2h_clears": 2,
        "h2h_avg_total": 220.0,
    }
    defaults.update(overrides)
    return TeamBetTotalsHitRateRow(**defaults)


PIPELINE_CASES = [
    pytest.param(
        "nba_spreads_snapshot_pipeline",
        "NbaSpreadsSnapshotPipeline",
        "basketball_nba",
        "spreads",
        "nba_spreads_v1",
        SpreadsSnapshotBuilder,
        _spreads_hit_rate_row,
        False,
        id="nba_spreads",
    ),
    pytest.param(
        "nba_totals_snapshot_pipeline",
        "NbaTotalsSnapshotPipeline",
        "basketball_nba",
        "totals",
        "nba_totals_v1",
        TotalsSnapshotBuilder,
        _totals_hit_rate_row,
        False,
        id="nba_totals",
    ),
    pytest.param(
        "mlb_h2h_snapshot_pipeline",
        "MlbH2hSnapshotPipeline",
        "baseball_mlb",
        "h2h",
        "mlb_h2h_v1",
        H2hSnapshotBuilder,
        _h2h_hit_rate_row,
        False,
        id="mlb_h2h",
    ),
    pytest.param(
        "mlb_spreads_snapshot_pipeline",
        "MlbSpreadsSnapshotPipeline",
        "baseball_mlb",
        "spreads",
        "mlb_spreads_v1",
        SpreadsSnapshotBuilder,
        _spreads_hit_rate_row,
        False,
        id="mlb_spreads",
    ),
    pytest.param(
        "mlb_totals_snapshot_pipeline",
        "MlbTotalsSnapshotPipeline",
        "baseball_mlb",
        "totals",
        "mlb_totals_v1",
        TotalsSnapshotBuilder,
        _totals_hit_rate_row,
        False,
        id="mlb_totals",
    ),
    pytest.param(
        "nfl_h2h_snapshot_pipeline",
        "NflH2hSnapshotPipeline",
        "americanfootball_nfl",
        "h2h",
        "nfl_h2h_v1",
        H2hSnapshotBuilder,
        _h2h_hit_rate_row,
        False,
        id="nfl_h2h",
    ),
    pytest.param(
        "nfl_spreads_snapshot_pipeline",
        "NflSpreadsSnapshotPipeline",
        "americanfootball_nfl",
        "spreads",
        "nfl_spreads_v1",
        SpreadsSnapshotBuilder,
        _spreads_hit_rate_row,
        False,
        id="nfl_spreads",
    ),
    pytest.param(
        "nfl_totals_snapshot_pipeline",
        "NflTotalsSnapshotPipeline",
        "americanfootball_nfl",
        "totals",
        "nfl_totals_v1",
        TotalsSnapshotBuilder,
        _totals_hit_rate_row,
        False,
        id="nfl_totals",
    ),
    pytest.param(
        "cfb_h2h_snapshot_pipeline",
        "CfbH2hSnapshotPipeline",
        "americanfootball_ncaaf",
        "h2h",
        "cfb_h2h_v1",
        H2hSnapshotBuilder,
        _h2h_hit_rate_row,
        True,
        id="cfb_h2h",
    ),
    pytest.param(
        "cfb_spreads_snapshot_pipeline",
        "CfbSpreadsSnapshotPipeline",
        "americanfootball_ncaaf",
        "spreads",
        "cfb_spreads_v1",
        SpreadsSnapshotBuilder,
        _spreads_hit_rate_row,
        True,
        id="cfb_spreads",
    ),
    pytest.param(
        "cfb_totals_snapshot_pipeline",
        "CfbTotalsSnapshotPipeline",
        "americanfootball_ncaaf",
        "totals",
        "cfb_totals_v1",
        TotalsSnapshotBuilder,
        _totals_hit_rate_row,
        True,
        id="cfb_totals",
    ),
]


def _load_pipeline(module_name: str, class_name: str):
    module = importlib.import_module(f"pipelines.team_bets.{module_name}")
    return getattr(module, class_name)


def _pipeline(
    module_name: str,
    class_name: str,
    builder,
    *,
    odds_rows=None,
    hit_rate_rows=None,
    insert_returns=None,
):
    pipeline_cls = _load_pipeline(module_name, class_name)
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

    return pipeline_cls(
        odds_repo=odds_repo,
        hit_rate_repo=hit_rate_repo,
        snapshot_repo=snapshot_repo,
        builder=builder(),
        now_fn=lambda: CREATED_AT,
    )


@pytest.mark.parametrize(
    "module_name,class_name,sport_key,market_key,snapshot_version,builder_cls,hit_rate_factory,cfb_skip",
    PIPELINE_CASES,
)
class TestTeamBetSnapshotPipelines:
    def test_snapshots_matching_odds_and_hit_rate_pair(
        self,
        module_name,
        class_name,
        sport_key,
        market_key,
        snapshot_version,
        builder_cls,
        hit_rate_factory,
        cfb_skip,
    ):
        if cfb_skip:
            pytest.skip("CFB upstream tables not wired yet")

        pipeline = _pipeline(
            module_name,
            class_name,
            builder_cls,
            odds_rows=[_odds_row(sport_key=sport_key, market_key=market_key)],
            hit_rate_rows=[hit_rate_factory()],
        )

        result = pipeline.run(
            SnapshotRequest(
                sport_key=sport_key,
                market_key=market_key,
                observation_time=OBSERVATION_TIME,
            ),
        )

        assert result == SnapshotRunResult(
            candidates=1,
            snapshotted=1,
            skipped_existing=0,
            skipped_leakage=0,
        )
        record = pipeline.snapshot_repo.insert_if_absent.call_args.args[0]
        assert record.snapshot_version == snapshot_version

    def test_passes_fixed_sport_and_market_to_odds_repo(
        self,
        module_name,
        class_name,
        sport_key,
        market_key,
        snapshot_version,
        builder_cls,
        hit_rate_factory,
        cfb_skip,
    ):
        if cfb_skip:
            pytest.skip("CFB upstream tables not wired yet")

        pipeline = _pipeline(module_name, class_name, builder_cls)
        pipeline.run(
            SnapshotRequest(
                sport_key=sport_key,
                market_key=market_key,
                observation_time=OBSERVATION_TIME,
            ),
        )

        pipeline.odds_repo.fetch_pregame_odds.assert_called_once_with(
            sport_key=sport_key,
            market_key=market_key,
            observation_time=OBSERVATION_TIME,
        )

    def test_rejects_mismatched_request(
        self,
        module_name,
        class_name,
        sport_key,
        market_key,
        snapshot_version,
        builder_cls,
        hit_rate_factory,
        cfb_skip,
    ):
        pipeline = _pipeline(module_name, class_name, builder_cls)

        with pytest.raises(ValueError, match=sport_key):
            pipeline.run(
                SnapshotRequest(
                    sport_key="basketball_nba" if sport_key != "basketball_nba" else "baseball_mlb",
                    market_key=market_key,
                    observation_time=OBSERVATION_TIME,
                ),
            )


CFB_PIPELINE_CASES = [case for case in PIPELINE_CASES if case.id.startswith("cfb_")]


@pytest.mark.parametrize(
    "module_name,class_name,sport_key,market_key,snapshot_version,builder_cls,hit_rate_factory,cfb_skip",
    CFB_PIPELINE_CASES,
)
class TestCfbSnapshotPipelines:
    def test_skips_until_upstream_tables_exist(
        self,
        module_name,
        class_name,
        sport_key,
        market_key,
        snapshot_version,
        builder_cls,
        hit_rate_factory,
        cfb_skip,
    ):
        pipeline = _pipeline(module_name, class_name, builder_cls)

        result = pipeline.run(
            SnapshotRequest(
                sport_key=sport_key,
                market_key=market_key,
                observation_time=OBSERVATION_TIME,
            ),
        )

        assert result == SnapshotRunResult(
            candidates=0,
            snapshotted=0,
            skipped_existing=0,
            skipped_leakage=0,
        )
        pipeline.odds_repo.fetch_pregame_odds.assert_not_called()
        pipeline.hit_rate_repo.fetch_pregame_hit_rates.assert_not_called()
