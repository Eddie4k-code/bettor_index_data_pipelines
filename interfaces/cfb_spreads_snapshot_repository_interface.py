"""ABC for append-only CFB spreads snapshot persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import CfbSpreadsSnapshotRecord


class CfbSpreadsSnapshotRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: CfbSpreadsSnapshotRecord) -> bool:
        """Insert the row when PK is absent; return False when it already exists."""
