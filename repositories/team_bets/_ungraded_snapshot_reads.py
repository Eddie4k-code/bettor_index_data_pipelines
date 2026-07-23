"""Shared LEFT JOIN query for snapshot rows without a matching grade."""

from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

TRecord = TypeVar("TRecord", bound=BaseModel)


def fetch_ungraded_snapshots(
    db: Session,
    *,
    snapshot_model: type,
    grade_model: type,
    record_cls: type[TRecord],
    event_id: str | None = None,
    as_of: datetime | None = None,
) -> list[TRecord]:
    query = (
        db.query(snapshot_model)
        .outerjoin(
            grade_model,
            (snapshot_model.observation_time == grade_model.observation_time)
            & (snapshot_model.event_id == grade_model.event_id)
            & (snapshot_model.bookmaker == grade_model.bookmaker)
            & (snapshot_model.outcome_name == grade_model.outcome_name)
            & (snapshot_model.snapshot_version == grade_model.snapshot_version),
        )
        .filter(grade_model.observation_time.is_(None))
    )
    if event_id is not None:
        query = query.filter(snapshot_model.event_id == event_id)
    if as_of is not None:
        query = query.filter(snapshot_model.commence_time <= as_of)
    return [record_cls.model_validate(row) for row in query.all()]
