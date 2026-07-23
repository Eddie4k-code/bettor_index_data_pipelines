"""ABC for read-only NFL H2H snapshot lookups for grading."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.team_bets import NflH2hSnapshotRecord


class NflH2hSnapshotReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[NflH2hSnapshotRecord]:
        """Return snapshot rows that have started and lack a grade row."""
