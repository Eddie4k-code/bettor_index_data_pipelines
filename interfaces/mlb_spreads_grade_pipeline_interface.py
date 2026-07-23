"""ABC for the MLB spreads grade orchestrator."""

from abc import ABC, abstractmethod

from schemas.grade import GradeRequest, GradeRunResult


class MlbSpreadsGradePipelineInterface(ABC):
    @abstractmethod
    def run(self, request: GradeRequest) -> GradeRunResult:
        """Grade completed MLB spreads snapshot rows."""
