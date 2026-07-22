"""ABC for append-only NFL totals snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NflTotalsSnapshotRecord


class NflTotalsSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NflTotalsSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
