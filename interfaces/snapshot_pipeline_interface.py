"""Contract for the snapshot orchestration layer."""

from abc import ABC, abstractmethod

from schemas.snapshot import SnapshotRequest, SnapshotRunResult


class SnapshotPipelineInterface(ABC):
    """Runs a pregame snapshot for one sport/market at ``observation_time``."""

    @abstractmethod
    def run(self, request: SnapshotRequest) -> SnapshotRunResult:
        """Validate the request, route by sport/market, and persist snapshot rows."""
        pass
