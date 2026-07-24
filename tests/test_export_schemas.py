"""Tests for shared team-bet export request/result and manifest shapes."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from schemas.export import (
    EXPORT_LABEL_COLUMNS,
    ExportManifest,
    ExportRequest,
    ExportRunResult,
)


def test_export_label_columns_are_stable_training_drop_set():
    assert EXPORT_LABEL_COLUMNS == (
        "grade_outcome",
        "grade_version",
        "home_team_score",
        "away_team_score",
        "graded_at",
    )


def test_export_request_preserves_optional_temporal_filters():
    observation_start = datetime(2025, 10, 1, 0, 0, tzinfo=timezone.utc)
    observation_end = datetime(2025, 10, 31, 0, 0, tzinfo=timezone.utc)
    commence_start = datetime(2025, 10, 1, 0, 0, tzinfo=timezone.utc)
    commence_end = datetime(2026, 4, 1, 0, 0, tzinfo=timezone.utc)

    request = ExportRequest(
        sport_key="basketball_nba",
        market_key="h2h",
        output_dir="exports",
        observation_time_start=observation_start,
        observation_time_end=observation_end,
        commence_time_start=commence_start,
        commence_time_end=commence_end,
    )

    assert request.observation_time_start == observation_start
    assert request.observation_time_end == observation_end
    assert request.commence_time_start == commence_start
    assert request.commence_time_end == commence_end


def test_export_request_is_frozen():
    request = ExportRequest(
        sport_key="basketball_nba",
        market_key="h2h",
        output_dir="exports",
    )

    with pytest.raises(ValidationError):
        request.output_dir = "other"


def test_export_run_result_is_frozen():
    result = ExportRunResult(
        candidates=100,
        exported=95,
        partitions_written=3,
        skipped_empty=1,
    )

    assert result.exported == 95

    with pytest.raises(ValidationError):
        result.exported = 96


def test_export_manifest_records_filter_bounds_and_versions():
    exported_at = datetime(2026, 7, 23, 1, 0, tzinfo=timezone.utc)

    manifest = ExportManifest(
        row_count=42,
        sport_key="basketball_nba",
        market_key="h2h",
        observation_time_start=datetime(2025, 10, 1, 0, 0, tzinfo=timezone.utc),
        observation_time_end=datetime(2025, 10, 31, 0, 0, tzinfo=timezone.utc),
        commence_time_start=datetime(2025, 10, 1, 0, 0, tzinfo=timezone.utc),
        commence_time_end=datetime(2026, 4, 1, 0, 0, tzinfo=timezone.utc),
        snapshot_versions=["nba_h2h_v1"],
        grade_versions=["nba_h2h_grade_v1"],
        feature_columns=["outcome_price", "hit_rate_10"],
        label_columns=list(EXPORT_LABEL_COLUMNS),
        git_sha="abc123",
        exported_at=exported_at,
    )

    assert manifest.row_count == 42
    assert manifest.snapshot_versions == ["nba_h2h_v1"]
    assert manifest.label_columns == list(EXPORT_LABEL_COLUMNS)
    assert manifest.git_sha == "abc123"
    assert manifest.exported_at == exported_at
