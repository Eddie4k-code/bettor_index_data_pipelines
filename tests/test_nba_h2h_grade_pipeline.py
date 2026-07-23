"""Tests for the NBA H2H team-bet grade vertical slice (pipeline + mocked repos)."""

import logging
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from builders.team_bets.h2h_grade_builder import H2hGradeBuilder
from pipelines.team_bets import nba_h2h_grade_pipeline
from pipelines.team_bets.nba_h2h_grade_pipeline import NbaH2hGradePipeline
from schemas.games import CompletedGameRow
from schemas.grade import GradeRequest, GradeRunResult
from schemas.team_bets import NbaH2hGradeRecord, NbaH2hSnapshotRecord

OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)
GRADED_AT = datetime(2026, 7, 22, 4, 0, tzinfo=timezone.utc)
COMMENCE_TIME = datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc)


def _request(**overrides) -> GradeRequest:
    defaults = {
        "sport_key": "basketball_nba",
        "market_key": "h2h",
        "event_id": None,
    }
    defaults.update(overrides)
    return GradeRequest(**defaults)


def _snapshot(**overrides) -> NbaH2hSnapshotRecord:
    defaults = {
        "observation_time": OBSERVATION_TIME,
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "commence_time": COMMENCE_TIME,
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
        "last_n_wins": 7,
        "last_n_losses": 3,
        "last_n_sample": 10,
        "last_n_window": 10,
    }
    defaults.update(overrides)
    return NbaH2hSnapshotRecord(**defaults)


def _completed_game(**overrides) -> CompletedGameRow:
    defaults = {
        "sport_key": "basketball_nba",
        "status": "finished",
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "home_team_id": 1,
        "away_team_id": 2,
        "home_team_score": 112,
        "away_team_score": 105,
        "date": datetime(2026, 7, 21, 23, 30, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return CompletedGameRow(**defaults)


def _pipeline(
    *,
    snapshots=None,
    game=None,
    insert_returns=None,
    now_fn=None,
) -> NbaH2hGradePipeline:
    snapshot_read_repo = MagicMock()
    snapshot_read_repo.fetch_ungraded_candidates.return_value = (
        snapshots if snapshots is not None else []
    )

    games_repo = MagicMock()
    games_repo.fetch_completed_game.return_value = game

    grade_repo = MagicMock()
    if insert_returns is None:
        grade_repo.insert_if_absent.return_value = True
    else:
        grade_repo.insert_if_absent.side_effect = insert_returns

    return NbaH2hGradePipeline(
        snapshot_read_repo=snapshot_read_repo,
        games_repo=games_repo,
        grade_repo=grade_repo,
        builder=H2hGradeBuilder(),
        now_fn=now_fn or (lambda: GRADED_AT),
    )


class TestNbaH2hGradePipeline:
    def test_grades_ungraded_snapshot_with_completed_game(self):
        pipeline = _pipeline(
            snapshots=[_snapshot()],
            game=_completed_game(),
        )

        result = pipeline.run(_request())

        assert result == GradeRunResult(
            candidates=1,
            graded=1,
            skipped_existing=0,
            skipped_ungradeable=0,
        )
        pipeline.grade_repo.insert_if_absent.assert_called_once()
        record = pipeline.grade_repo.insert_if_absent.call_args.args[0]
        assert isinstance(record, NbaH2hGradeRecord)
        assert record.grade_version == "nba_h2h_grade_v1"
        assert record.grade_outcome == "win"

    def test_skips_existing_grade_rows(self):
        pipeline = _pipeline(
            snapshots=[_snapshot()],
            game=_completed_game(),
            insert_returns=[False],
        )

        result = pipeline.run(_request())

        assert result.graded == 0
        assert result.skipped_existing == 1

    def test_skips_when_completed_game_missing(self):
        pipeline = _pipeline(
            snapshots=[_snapshot()],
            game=None,
        )

        result = pipeline.run(_request())

        assert result.graded == 0
        assert result.skipped_ungradeable == 1
        pipeline.grade_repo.insert_if_absent.assert_not_called()

    def test_skips_when_team_ids_missing(self):
        pipeline = _pipeline(
            snapshots=[_snapshot(home_team_id=None, away_team_id=None)],
            game=_completed_game(),
        )

        result = pipeline.run(_request())

        assert result.skipped_ungradeable == 1
        pipeline.games_repo.fetch_completed_game.assert_not_called()

    def test_passes_event_id_filter_to_snapshot_read_repo(self):
        pipeline = _pipeline()

        pipeline.run(_request(event_id="evt-1"))

        pipeline.snapshot_read_repo.fetch_ungraded_candidates.assert_called_once_with(
            event_id="evt-1",
            as_of=GRADED_AT,
        )

    def test_passes_matchup_to_games_repo(self):
        pipeline = _pipeline(
            snapshots=[_snapshot()],
            game=_completed_game(),
        )

        pipeline.run(_request())

        pipeline.games_repo.fetch_completed_game.assert_called_once_with(
            sport_key="basketball_nba",
            event_id="evt-1",
            home_team_id=1,
            away_team_id=2,
            commence_time=COMMENCE_TIME,
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
            pipeline.run(_request(sport_key=sport_key, market_key=market_key))


class TestNbaH2hGradePipelineLogging:
    def test_logs_run_lifecycle_at_info(self, caplog):
        caplog.set_level(logging.INFO, logger=nba_h2h_grade_pipeline.logger.name)
        pipeline = _pipeline(
            snapshots=[_snapshot()],
            game=_completed_game(),
        )

        pipeline.run(_request())

        messages = [record.getMessage() for record in caplog.records]
        assert any("Starting NBA H2H grade run" in message for message in messages)
        assert any("Fetched ungraded snapshot candidates" in message for message in messages)
        assert any("NBA H2H grade run complete" in message for message in messages)
        assert any("graded=1" in message for message in messages)
