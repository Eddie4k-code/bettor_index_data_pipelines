"""ABC for append-only NBA spreads snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NbaSpreadsSnapshotRecord


class NbaSpreadsSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NbaSpreadsSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
