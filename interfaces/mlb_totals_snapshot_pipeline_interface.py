"""ABC for the MLB totals snapshot orchestrator."""

from abc import ABC, abstractmethod

from schemas.snapshot import SnapshotRequest, SnapshotRunResult


class MlbTotalsSnapshotPipelineInterface(ABC):
    @abstractmethod
    def run(self, request: SnapshotRequest) -> SnapshotRunResult:
        """Build and persist MLB totals pregame snapshots for one observation time."""
