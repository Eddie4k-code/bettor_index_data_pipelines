"""ABC for the CFB H2H snapshot orchestrator."""

from abc import ABC, abstractmethod

from schemas.snapshot import SnapshotRequest, SnapshotRunResult


class CfbH2hSnapshotPipelineInterface(ABC):
    @abstractmethod
    def run(self, request: SnapshotRequest) -> SnapshotRunResult:
        """Build and persist CFB H2H pregame snapshots for one observation time."""
