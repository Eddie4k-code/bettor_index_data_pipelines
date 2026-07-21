"""Contract for append-only writes to ``mlb_batter_hits_pregame_snapshots``."""

from abc import ABC, abstractmethod

from schemas.mlb_batter_hits_snapshot import MLBBatterHitsSnapshotRecord
from schemas.snapshot import SnapshotInsertResult


class MLBBatterHitsSnapshotRepositoryInterface(ABC):
    """Persists batter_hits snapshot rows without updating existing PKs."""

    @abstractmethod
    def insert_snapshots(
        self,
        records: list[MLBBatterHitsSnapshotRecord],
    ) -> SnapshotInsertResult:
        """Append snapshot rows; skip duplicates keyed by observation_time + market identity."""
        pass
