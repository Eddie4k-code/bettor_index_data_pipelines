"""Shared team-bet grade request/result shapes and base post-game label fields."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

GradeOutcome = Literal["win", "loss", "push", "void"]


class GradeRequest(BaseModel):
    """Input to the grade pipeline for one sport/market with an optional event filter."""

    model_config = ConfigDict(frozen=True)

    sport_key: str
    market_key: str
    event_id: str | None = None


class GradeRunResult(BaseModel):
    """Aggregate counts logged after a grade pipeline run."""

    model_config = ConfigDict(frozen=True)

    candidates: int
    graded: int
    skipped_existing: int
    skipped_ungradeable: int


class TeamBetGradeRecordBase(BaseModel):
    """Fields shared by every persisted team-bet post-game grade row."""

    model_config = ConfigDict(from_attributes=True, frozen=True, extra="forbid")

    observation_time: datetime
    event_id: str
    sport_key: str
    market_key: str
    bookmaker: str
    outcome_name: str
    snapshot_version: str
    grade_outcome: GradeOutcome
    grade_version: str
    home_team_score: int | None
    away_team_score: int | None
    outcome_point: float | None
    commence_time: datetime
    graded_at: datetime
    created_at: datetime
