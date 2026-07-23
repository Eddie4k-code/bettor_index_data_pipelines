"""Tests for shared team-bet grade request/result and base record fields."""

from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from schemas.grade import (
    GradeOutcome,
    GradeRequest,
    GradeRunResult,
    TeamBetGradeRecordBase,
)
from schemas.team_bets import (
    CfbH2hGradeRecord,
    CfbSpreadsGradeRecord,
    CfbTotalsGradeRecord,
    MlbH2hGradeRecord,
    MlbSpreadsGradeRecord,
    MlbTotalsGradeRecord,
    NbaH2hGradeRecord,
    NbaSpreadsGradeRecord,
    NbaTotalsGradeRecord,
    NflH2hGradeRecord,
    NflSpreadsGradeRecord,
    NflTotalsGradeRecord,
)


def _base_grade_kwargs(**overrides):
    defaults = {
        "observation_time": datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc),
        "event_id": "evt-1",
        "sport_key": "basketball_nba",
        "market_key": "h2h",
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "snapshot_version": "nba_h2h_v1",
        "grade_outcome": "win",
        "grade_version": "nba_h2h_grade_v1",
        "home_team_score": 110,
        "away_team_score": 102,
        "outcome_point": None,
        "commence_time": datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc),
        "graded_at": datetime(2026, 7, 22, 2, 0, tzinfo=timezone.utc),
        "created_at": datetime(2026, 7, 22, 2, 5, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return defaults


@pytest.mark.parametrize(
    "outcome",
    ["win", "loss", "push", "void"],
)
def test_grade_outcome_accepts_allowed_values(outcome):
    record = TeamBetGradeRecordBase(**_base_grade_kwargs(grade_outcome=outcome))

    assert record.grade_outcome == outcome


def test_grade_outcome_rejects_invalid_value():
    with pytest.raises(ValidationError):
        TeamBetGradeRecordBase(**_base_grade_kwargs(grade_outcome="pending"))


def test_grade_request_preserves_optional_event_id_filter():
    request = GradeRequest(
        sport_key="americanfootball_nfl",
        market_key="spreads",
        event_id="evt-99",
    )

    assert request.event_id == "evt-99"


def test_grade_request_is_frozen():
    request = GradeRequest(
        sport_key="basketball_nba",
        market_key="h2h",
    )

    with pytest.raises(ValidationError):
        request.sport_key = "baseball_mlb"


def test_team_bet_grade_record_base_accepts_required_fields():
    record = TeamBetGradeRecordBase(**_base_grade_kwargs(outcome_point=-3.5))

    assert record.home_team_score == 110
    assert record.outcome_point == -3.5


def test_team_bet_grade_record_base_rejects_snapshot_feature_fields():
    with pytest.raises(ValidationError):
        TeamBetGradeRecordBase(
            **_base_grade_kwargs(
                outcome_price=-110.0,
                home_team="Boston Celtics",
            ),
        )


def test_team_bet_grade_record_base_is_frozen():
    record = TeamBetGradeRecordBase(**_base_grade_kwargs())

    with pytest.raises(ValidationError):
        record.grade_outcome = "loss"


def test_grade_run_result_is_frozen():
    result = GradeRunResult(
        candidates=10,
        graded=8,
        skipped_existing=1,
        skipped_ungradeable=1,
    )

    assert result.graded == 8

    with pytest.raises(ValidationError):
        result.graded = 9


GRADE_RECORD_CONSTANTS = [
    pytest.param(
        NbaH2hGradeRecord,
        "basketball_nba",
        "h2h",
        "nba_h2h_grade_v1",
        id="nba_h2h",
    ),
    pytest.param(
        NbaSpreadsGradeRecord,
        "basketball_nba",
        "spreads",
        "nba_spreads_grade_v1",
        id="nba_spreads",
    ),
    pytest.param(
        NbaTotalsGradeRecord,
        "basketball_nba",
        "totals",
        "nba_totals_grade_v1",
        id="nba_totals",
    ),
    pytest.param(
        MlbH2hGradeRecord,
        "baseball_mlb",
        "h2h",
        "mlb_h2h_grade_v1",
        id="mlb_h2h",
    ),
    pytest.param(
        MlbSpreadsGradeRecord,
        "baseball_mlb",
        "spreads",
        "mlb_spreads_grade_v1",
        id="mlb_spreads",
    ),
    pytest.param(
        MlbTotalsGradeRecord,
        "baseball_mlb",
        "totals",
        "mlb_totals_grade_v1",
        id="mlb_totals",
    ),
    pytest.param(
        NflH2hGradeRecord,
        "americanfootball_nfl",
        "h2h",
        "nfl_h2h_grade_v1",
        id="nfl_h2h",
    ),
    pytest.param(
        NflSpreadsGradeRecord,
        "americanfootball_nfl",
        "spreads",
        "nfl_spreads_grade_v1",
        id="nfl_spreads",
    ),
    pytest.param(
        NflTotalsGradeRecord,
        "americanfootball_nfl",
        "totals",
        "nfl_totals_grade_v1",
        id="nfl_totals",
    ),
    pytest.param(
        CfbH2hGradeRecord,
        "americanfootball_ncaaf",
        "h2h",
        "cfb_h2h_grade_v1",
        id="cfb_h2h",
    ),
    pytest.param(
        CfbSpreadsGradeRecord,
        "americanfootball_ncaaf",
        "spreads",
        "cfb_spreads_grade_v1",
        id="cfb_spreads",
    ),
    pytest.param(
        CfbTotalsGradeRecord,
        "americanfootball_ncaaf",
        "totals",
        "cfb_totals_grade_v1",
        id="cfb_totals",
    ),
]


@pytest.mark.parametrize(
    ("record_cls", "sport_key", "market_key", "grade_version"),
    GRADE_RECORD_CONSTANTS,
)
def test_grade_record_has_fixed_identity_defaults(
    record_cls,
    sport_key,
    market_key,
    grade_version,
):
    assert record_cls.model_fields["sport_key"].default == sport_key
    assert record_cls.model_fields["market_key"].default == market_key
    assert record_cls.model_fields["grade_version"].default == grade_version
