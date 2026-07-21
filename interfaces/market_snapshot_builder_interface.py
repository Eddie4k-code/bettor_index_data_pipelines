"""Contract for per-market snapshot assembly."""

from abc import ABC, abstractmethod

from schemas.snapshot import MarketSnapshotBuildResult, SnapshotRequest


class MarketSnapshotBuilderInterface(ABC):
    """Joins upstream read models into market-specific pregame snapshot records."""

    @abstractmethod
    def build_snapshots(self, request: SnapshotRequest) -> MarketSnapshotBuildResult:
        """Collect odds, join hit rates at observation_time, and return rows ready to persist."""
        pass
