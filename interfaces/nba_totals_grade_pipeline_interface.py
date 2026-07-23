"""ABC for the NBA totals grade orchestrator."""

from abc import ABC, abstractmethod

from schemas.grade import GradeRequest, GradeRunResult


class NbaTotalsGradePipelineInterface(ABC):
    @abstractmethod
    def run(self, request: GradeRequest) -> GradeRunResult:
        """Grade completed NBA totals snapshot rows."""
