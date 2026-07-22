"""ABC for append-only MLB spreads snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import MlbSpreadsSnapshotRecord


class MlbSpreadsSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: MlbSpreadsSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
