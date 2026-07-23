"""ABC for the MLB totals grade orchestrator."""

from abc import ABC, abstractmethod

from schemas.grade import GradeRequest, GradeRunResult


class MlbTotalsGradePipelineInterface(ABC):
    @abstractmethod
    def run(self, request: GradeRequest) -> GradeRunResult:
        """Grade completed MLB totals snapshot rows."""
