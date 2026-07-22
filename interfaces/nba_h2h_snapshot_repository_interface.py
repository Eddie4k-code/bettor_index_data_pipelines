"""ABC for append-only NBA H2H snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NbaH2hSnapshotRecord


class NbaH2hSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NbaH2hSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
