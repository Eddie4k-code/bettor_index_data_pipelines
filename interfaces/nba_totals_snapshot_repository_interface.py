"""ABC for append-only NBA totals snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NbaTotalsSnapshotRecord


class NbaTotalsSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NbaTotalsSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
