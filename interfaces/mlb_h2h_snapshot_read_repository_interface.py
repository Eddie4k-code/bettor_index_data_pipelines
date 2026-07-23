"""ABC for read-only MLB H2H snapshot lookups for grading."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.team_bets import MlbH2hSnapshotRecord


class MlbH2hSnapshotReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[MlbH2hSnapshotRecord]:
        """Return snapshot rows that have started and lack a grade row."""
