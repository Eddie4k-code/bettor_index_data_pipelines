"""ABC for the MLB H2H snapshot orchestrator."""

from abc import ABC, abstractmethod

from schemas.snapshot import SnapshotRequest, SnapshotRunResult


class MlbH2hSnapshotPipelineInterface(ABC):
    @abstractmethod
    def run(self, request: SnapshotRequest) -> SnapshotRunResult:
        """Build and persist MLB H2H pregame snapshots for one observation time."""
