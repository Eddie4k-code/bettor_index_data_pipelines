"""Tests for main.py snapshot and grade CLI subcommands."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

import main
from schemas.grade import GradeRequest, GradeRunResult
from schemas.snapshot import SnapshotRequest, SnapshotRunResult

OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)

EXPECTED_GRADE_SUBCOMMANDS = frozenset({
    "nba-h2h",
    "nba-spreads",
    "nba-totals",
    "mlb-h2h",
    "mlb-spreads",
    "mlb-totals",
    "nfl-h2h",
    "nfl-spreads",
    "nfl-totals",
    "cfb-h2h",
    "cfb-spreads",
    "cfb-totals",
})

EXPECTED_SNAPSHOT_SUBCOMMANDS = frozenset({
    "nba-h2h",
    "nba-spreads",
    "nba-totals",
    "mlb-h2h",
    "mlb-spreads",
    "mlb-totals",
    "nfl-h2h",
    "nfl-spreads",
    "nfl-totals",
    "cfb-h2h",
    "cfb-spreads",
    "cfb-totals",
})


class TestSnapshotSubcommandRegistry:
    def test_registry_contains_all_twelve_subcommands(self):
        assert set(main.SNAPSHOT_SPECS) == EXPECTED_SNAPSHOT_SUBCOMMANDS


class TestGradeSubcommandRegistry:
    def test_registry_contains_all_twelve_subcommands(self):
        assert set(main.GRADE_SPECS) == EXPECTED_GRADE_SUBCOMMANDS


class TestBuildParser:
    def test_parses_snapshot_subcommand_with_observation_time(self):
        args = main.build_parser().parse_args([
            "snapshot",
            "nba-h2h",
            "--observation-time",
            "2026-07-21T12:00:00Z",
        ])
        assert args.command == "snapshot"
        assert args.snapshot_type == "nba-h2h"
        assert args.observation_time == OBSERVATION_TIME

    @pytest.mark.parametrize("subcommand", sorted(EXPECTED_SNAPSHOT_SUBCOMMANDS))
    def test_each_snapshot_subcommand_is_registered(self, subcommand):
        parser = main.build_parser()
        args = parser.parse_args([
            "snapshot",
            subcommand,
            "--observation-time",
            "2026-07-21T12:00:00+00:00",
        ])
        assert args.snapshot_type == subcommand

    def test_requires_observation_time(self):
        with pytest.raises(SystemExit):
            main.build_parser().parse_args(["snapshot", "nba-h2h"])

    def test_parses_grade_subcommand_with_optional_event_id(self):
        args = main.build_parser().parse_args([
            "grade",
            "nba-h2h",
            "--event-id",
            "evt-1",
        ])
        assert args.command == "grade"
        assert args.grade_type == "nba-h2h"
        assert args.event_id == "evt-1"

    @pytest.mark.parametrize("subcommand", sorted(EXPECTED_GRADE_SUBCOMMANDS))
    def test_each_grade_subcommand_is_registered(self, subcommand):
        args = main.build_parser().parse_args(["grade", subcommand])
        assert args.grade_type == subcommand
        assert args.event_id is None


class TestParseObservationTime:
    def test_parses_z_suffix_as_utc(self):
        parsed = main.parse_observation_time("2026-07-21T12:00:00Z")
        assert parsed == OBSERVATION_TIME

    def test_parses_explicit_offset(self):
        parsed = main.parse_observation_time("2026-07-21T08:00:00-04:00")
        assert parsed == OBSERVATION_TIME

    def test_naive_datetime_gets_utc(self):
        parsed = main.parse_observation_time("2026-07-21T12:00:00")
        assert parsed == OBSERVATION_TIME


class TestRunSnapshot:
    def test_dispatches_pipeline_with_matching_request(self, mocker):
        mock_pipeline = MagicMock()
        mock_pipeline.run.return_value = SnapshotRunResult(
            candidates=2,
            snapshotted=1,
            skipped_existing=1,
            skipped_leakage=0,
        )
        mocker.patch("main.create_snapshot_pipeline", return_value=mock_pipeline)
        mock_db = MagicMock()
        mock_cm = MagicMock()
        mock_cm.__enter__.return_value = mock_db
        mock_cm.__exit__.return_value = False
        mocker.patch("main.get_db", return_value=mock_cm)
        mocker.patch("main.ensure_owned_tables")

        result = main.run_snapshot("nfl-spreads", OBSERVATION_TIME)

        assert result.snapshotted == 1
        mock_pipeline.run.assert_called_once_with(
            SnapshotRequest(
                sport_key="americanfootball_nfl",
                market_key="spreads",
                observation_time=OBSERVATION_TIME,
            ),
        )
        main.ensure_owned_tables.assert_called_once_with(mock_db)

    def test_rejects_unknown_subcommand(self):
        with pytest.raises(ValueError, match="Unknown snapshot subcommand"):
            main.run_snapshot("nba-moneyline", OBSERVATION_TIME)


class TestRunGrade:
    def test_dispatches_pipeline_with_matching_request(self, mocker):
        mock_pipeline = MagicMock()
        mock_pipeline.run.return_value = GradeRunResult(
            candidates=2,
            graded=1,
            skipped_existing=1,
            skipped_ungradeable=0,
        )
        mocker.patch("main.create_grade_pipeline", return_value=mock_pipeline)
        mock_db = MagicMock()
        mock_cm = MagicMock()
        mock_cm.__enter__.return_value = mock_db
        mock_cm.__exit__.return_value = False
        mocker.patch("main.get_db", return_value=mock_cm)
        mocker.patch("main.ensure_owned_tables")

        result = main.run_grade("nfl-spreads", "evt-9")

        assert result.graded == 1
        mock_pipeline.run.assert_called_once_with(
            GradeRequest(
                sport_key="americanfootball_nfl",
                market_key="spreads",
                event_id="evt-9",
            ),
        )
        main.ensure_owned_tables.assert_called_once_with(mock_db)

    def test_rejects_unknown_subcommand(self):
        with pytest.raises(ValueError, match="Unknown grade subcommand"):
            main.run_grade("nba-moneyline")


class TestMain:
    def test_main_runs_snapshot_subcommand(self, mocker, capsys):
        mocker.patch(
            "main.run_snapshot",
            return_value=SnapshotRunResult(
                candidates=3,
                snapshotted=2,
                skipped_existing=1,
                skipped_leakage=0,
            ),
        )
        exit_code = main.main([
            "snapshot",
            "mlb-totals",
            "--observation-time",
            "2026-07-21T12:00:00Z",
        ])
        assert exit_code == 0
        main.run_snapshot.assert_called_once_with("mlb-totals", OBSERVATION_TIME)
        assert "snapshotted=2" in capsys.readouterr().out

    def test_main_runs_grade_subcommand(self, mocker, capsys):
        mocker.patch(
            "main.run_grade",
            return_value=GradeRunResult(
                candidates=3,
                graded=2,
                skipped_existing=1,
                skipped_ungradeable=0,
            ),
        )
        exit_code = main.main(["grade", "mlb-totals"])
        assert exit_code == 0
        main.run_grade.assert_called_once_with("mlb-totals", None)
        assert "graded=2" in capsys.readouterr().out
