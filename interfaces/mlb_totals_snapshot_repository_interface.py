"""ABC for append-only MLB totals snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import MlbTotalsSnapshotRecord


class MlbTotalsSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: MlbTotalsSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
