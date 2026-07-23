"""ABC for read-only MLB spreads snapshot lookups for grading."""

from abc import ABC, abstractmethod
from datetime import datetime

from schemas.team_bets import MlbSpreadsSnapshotRecord


class MlbSpreadsSnapshotReadRepositoryInterface(ABC):
    @abstractmethod
    def fetch_ungraded_candidates(
        self,
        *,
        event_id: str | None = None,
        as_of: datetime | None = None,
    ) -> list[MlbSpreadsSnapshotRecord]:
        """Return snapshot rows that have started and lack a grade row."""
