"""ABC for the NBA totals snapshot orchestrator."""

from abc import ABC, abstractmethod

from schemas.snapshot import SnapshotRequest, SnapshotRunResult


class NbaTotalsSnapshotPipelineInterface(ABC):
    @abstractmethod
    def run(self, request: SnapshotRequest) -> SnapshotRunResult:
        """Build and persist NBA totals pregame snapshots for one observation time."""
