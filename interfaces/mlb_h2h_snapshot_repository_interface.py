"""ABC for append-only MLB H2H snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import MlbH2hSnapshotRecord


class MlbH2hSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: MlbH2hSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
