"""ABC for read-only NBA spreads snapshot lookups for grading."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.team_bets import NbaSpreadsSnapshotRecord


class NbaSpreadsSnapshotReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[NbaSpreadsSnapshotRecord]:
        """Return snapshot rows that have started and lack a grade row."""
