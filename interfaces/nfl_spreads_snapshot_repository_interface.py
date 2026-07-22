"""ABC for append-only NFL spreads snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NflSpreadsSnapshotRecord


class NflSpreadsSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NflSpreadsSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
