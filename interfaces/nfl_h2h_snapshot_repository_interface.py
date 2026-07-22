"""ABC for append-only NFL H2H snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NflH2hSnapshotRecord


class NflH2hSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NflH2hSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
