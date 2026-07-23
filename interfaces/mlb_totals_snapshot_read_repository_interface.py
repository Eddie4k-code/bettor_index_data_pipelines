"""ABC for read-only MLB totals snapshot lookups for grading."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.team_bets import MlbTotalsSnapshotRecord


class MlbTotalsSnapshotReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[MlbTotalsSnapshotRecord]:
        """Return snapshot rows that have started and lack a grade row."""
