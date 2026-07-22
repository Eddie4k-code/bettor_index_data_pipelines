"""ABC for the CFB spreads snapshot orchestrator."""

from abc import ABC, abstractmethod

from schemas.snapshot import SnapshotRequest, SnapshotRunResult


class CfbSpreadsSnapshotPipelineInterface(ABC):
    @abstractmethod
    def run(self, request: SnapshotRequest) -> SnapshotRunResult:
        """Build and persist CFB spreads pregame snapshots for one observation time."""
