"""Parametrized tests for explicit team-bet grade pipelines (11 non-NBA-H2H slices)."""

import importlib
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from builders.team_bets.h2h_grade_builder import H2hGradeBuilder
from builders.team_bets.spreads_grade_builder import SpreadsGradeBuilder
from builders.team_bets.totals_grade_builder import TotalsGradeBuilder
from schemas.games import CompletedGameRow
from schemas.grade import GradeRequest, GradeRunResult

GRADED_AT = datetime(2026, 7, 22, 4, 0, tzinfo=timezone.utc)
OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)
COMMENCE_TIME = datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc)


def _completed_game(*, sport_key: str) -> CompletedGameRow:
    return CompletedGameRow(
        sport_key=sport_key,
        status="finished" if sport_key == "basketball_nba" else "final",
        home_team="Boston Celtics",
        away_team="Los Angeles Lakers",
        home_team_id=1,
        away_team_id=2,
        home_team_score=112,
        away_team_score=105,
        date=datetime(2026, 7, 21, 23, 30, tzinfo=timezone.utc),
    )


def _snapshot_fields(*, sport_key: str, market_key: str, **overrides):
    defaults = {
        "observation_time": OBSERVATION_TIME,
        "event_id": "evt-1",
        "sport_key": sport_key,
        "market_key": market_key,
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "commence_time": COMMENCE_TIME,
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
    if market_key == "spreads":
        defaults["outcome_point"] = -3.5
        defaults["spread"] = -3.5
        defaults["last_n_covers"] = 6
        defaults["last_n_sample"] = 10
        defaults["last_n_window"] = 10
        defaults["h2h_covers"] = 2
        defaults["h2h_sample"] = 3
        defaults["h2h_window"] = 10
        defaults["venue_covers"] = 4
        defaults["venue_sample"] = 5
        defaults["venue_window"] = 10
        defaults["venue_type"] = "home"
    elif market_key == "totals":
        defaults["outcome_name"] = "Over"
        defaults["outcome_point"] = 216.5
        defaults["direction"] = "Over"
        defaults["line"] = 216.5
        defaults["configured_window"] = 10
        defaults["home_team_clears"] = 6
        defaults["home_team_sample"] = 10
        defaults["away_team_clears"] = 5
        defaults["away_team_sample"] = 10
        defaults["h2h_window"] = 10
        defaults["h2h_sample"] = 3
        defaults["h2h_clears"] = 2
        defaults["h2h_avg_total"] = 218.3
        defaults["outcome_team_id"] = None
    else:
        defaults["outcome_point"] = None
        defaults["last_n_wins"] = 7
        defaults["last_n_losses"] = 3
        defaults["last_n_sample"] = 10
        defaults["last_n_window"] = 10
    defaults.update(overrides)
    return defaults


PIPELINE_CASES = [
    pytest.param(
        "nba_spreads_grade_pipeline",
        "NbaSpreadsGradePipeline",
        "basketball_nba",
        "spreads",
        "nba_spreads_grade_v1",
        SpreadsGradeBuilder,
        "NbaSpreadsSnapshotRecord",
        False,
        id="nba_spreads",
    ),
    pytest.param(
        "nba_totals_grade_pipeline",
        "NbaTotalsGradePipeline",
        "basketball_nba",
        "totals",
        "nba_totals_grade_v1",
        TotalsGradeBuilder,
        "NbaTotalsSnapshotRecord",
        False,
        id="nba_totals",
    ),
    pytest.param(
        "mlb_h2h_grade_pipeline",
        "MlbH2hGradePipeline",
        "baseball_mlb",
        "h2h",
        "mlb_h2h_grade_v1",
        H2hGradeBuilder,
        "MlbH2hSnapshotRecord",
        False,
        id="mlb_h2h",
    ),
    pytest.param(
        "mlb_spreads_grade_pipeline",
        "MlbSpreadsGradePipeline",
        "baseball_mlb",
        "spreads",
        "mlb_spreads_grade_v1",
        SpreadsGradeBuilder,
        "MlbSpreadsSnapshotRecord",
        False,
        id="mlb_spreads",
    ),
    pytest.param(
        "mlb_totals_grade_pipeline",
        "MlbTotalsGradePipeline",
        "baseball_mlb",
        "totals",
        "mlb_totals_grade_v1",
        TotalsGradeBuilder,
        "MlbTotalsSnapshotRecord",
        False,
        id="mlb_totals",
    ),
    pytest.param(
        "nfl_h2h_grade_pipeline",
        "NflH2hGradePipeline",
        "americanfootball_nfl",
        "h2h",
        "nfl_h2h_grade_v1",
        H2hGradeBuilder,
        "NflH2hSnapshotRecord",
        False,
        id="nfl_h2h",
    ),
    pytest.param(
        "nfl_spreads_grade_pipeline",
        "NflSpreadsGradePipeline",
        "americanfootball_nfl",
        "spreads",
        "nfl_spreads_grade_v1",
        SpreadsGradeBuilder,
        "NflSpreadsSnapshotRecord",
        False,
        id="nfl_spreads",
    ),
    pytest.param(
        "nfl_totals_grade_pipeline",
        "NflTotalsGradePipeline",
        "americanfootball_nfl",
        "totals",
        "nfl_totals_grade_v1",
        TotalsGradeBuilder,
        "NflTotalsSnapshotRecord",
        False,
        id="nfl_totals",
    ),
    pytest.param(
        "cfb_h2h_grade_pipeline",
        "CfbH2hGradePipeline",
        "americanfootball_ncaaf",
        "h2h",
        "cfb_h2h_grade_v1",
        H2hGradeBuilder,
        "CfbH2hSnapshotRecord",
        True,
        id="cfb_h2h",
    ),
    pytest.param(
        "cfb_spreads_grade_pipeline",
        "CfbSpreadsGradePipeline",
        "americanfootball_ncaaf",
        "spreads",
        "cfb_spreads_grade_v1",
        SpreadsGradeBuilder,
        "CfbSpreadsSnapshotRecord",
        True,
        id="cfb_spreads",
    ),
    pytest.param(
        "cfb_totals_grade_pipeline",
        "CfbTotalsGradePipeline",
        "americanfootball_ncaaf",
        "totals",
        "cfb_totals_grade_v1",
        TotalsGradeBuilder,
        "CfbTotalsSnapshotRecord",
        True,
        id="cfb_totals",
    ),
]


def _load_pipeline(module_name: str, class_name: str):
    module = importlib.import_module(f"pipelines.team_bets.{module_name}")
    return getattr(module, class_name)


def _load_snapshot_record(record_name: str):
    module = importlib.import_module("schemas.team_bets")
    return getattr(module, record_name)


def _pipeline(
    module_name: str,
    class_name: str,
    builder,
    *,
    snapshot_record_name: str,
    sport_key: str,
    market_key: str,
    snapshots=None,
    game=None,
):
    snapshot_record_cls = _load_snapshot_record(snapshot_record_name)
    pipeline_cls = _load_pipeline(module_name, class_name)

    snapshot_read_repo = MagicMock()
    snapshot_read_repo.fetch_ungraded_candidates.return_value = (
        [snapshot_record_cls(**_snapshot_fields(sport_key=sport_key, market_key=market_key))]
        if snapshots is None
        else snapshots
    )

    games_repo = MagicMock()
    games_repo.fetch_completed_game.return_value = game or _completed_game(sport_key=sport_key)

    grade_repo = MagicMock()
    grade_repo.insert_if_absent.return_value = True

    return pipeline_cls(
        snapshot_read_repo=snapshot_read_repo,
        games_repo=games_repo,
        grade_repo=grade_repo,
        builder=builder(),
        now_fn=lambda: GRADED_AT,
    )


@pytest.mark.parametrize(
    "module_name,class_name,sport_key,market_key,grade_version,builder_cls,snapshot_record_name,cfb_skip",
    PIPELINE_CASES,
)
class TestTeamBetGradePipelines:
    def test_grades_ungraded_snapshot(
        self,
        module_name,
        class_name,
        sport_key,
        market_key,
        grade_version,
        builder_cls,
        snapshot_record_name,
        cfb_skip,
    ):
        if cfb_skip:
            pytest.skip("CFB upstream tables not wired yet")

        pipeline = _pipeline(
            module_name,
            class_name,
            builder_cls,
            snapshot_record_name=snapshot_record_name,
            sport_key=sport_key,
            market_key=market_key,
        )

        result = pipeline.run(
            GradeRequest(
                sport_key=sport_key,
                market_key=market_key,
            ),
        )

        assert result == GradeRunResult(
            candidates=1,
            graded=1,
            skipped_existing=0,
            skipped_ungradeable=0,
        )
        record = pipeline.grade_repo.insert_if_absent.call_args.args[0]
        assert record.grade_version == grade_version

    def test_rejects_mismatched_request(
        self,
        module_name,
        class_name,
        sport_key,
        market_key,
        grade_version,
        builder_cls,
        snapshot_record_name,
        cfb_skip,
    ):
        pipeline = _pipeline(
            module_name,
            class_name,
            builder_cls,
            snapshot_record_name=snapshot_record_name,
            sport_key=sport_key,
            market_key=market_key,
            snapshots=[],
            game=None,
        )

        with pytest.raises(ValueError, match=sport_key):
            pipeline.run(
                GradeRequest(
                    sport_key="basketball_nba" if sport_key != "basketball_nba" else "baseball_mlb",
                    market_key=market_key,
                ),
            )


CFB_PIPELINE_CASES = [case for case in PIPELINE_CASES if case.id.startswith("cfb_")]


@pytest.mark.parametrize(
    "module_name,class_name,sport_key,market_key,grade_version,builder_cls,snapshot_record_name,cfb_skip",
    CFB_PIPELINE_CASES,
)
class TestCfbGradePipelines:
    def test_skips_until_upstream_tables_exist(
        self,
        module_name,
        class_name,
        sport_key,
        market_key,
        grade_version,
        builder_cls,
        snapshot_record_name,
        cfb_skip,
    ):
        pipeline = _pipeline(
            module_name,
            class_name,
            builder_cls,
            snapshot_record_name=snapshot_record_name,
            sport_key=sport_key,
            market_key=market_key,
            snapshots=[],
            game=None,
        )

        result = pipeline.run(
            GradeRequest(
                sport_key=sport_key,
                market_key=market_key,
            ),
        )

        assert result == GradeRunResult(
            candidates=0,
            graded=0,
            skipped_existing=0,
            skipped_ungradeable=0,
        )
        pipeline.snapshot_read_repo.fetch_ungraded_candidates.assert_not_called()
        pipeline.games_repo.fetch_completed_game.assert_not_called()
