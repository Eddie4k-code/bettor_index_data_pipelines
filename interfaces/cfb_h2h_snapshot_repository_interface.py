"""ABC for append-only CFB H2H snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import CfbH2hSnapshotRecord


class CfbH2hSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: CfbH2hSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
