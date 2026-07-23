"""ABC for the NBA spreads grade orchestrator."""

from abc import ABC, abstractmethod

from schemas.grade import GradeRequest, GradeRunResult


class NbaSpreadsGradePipelineInterface(ABC):
    @abstractmethod
    def run(self, request: GradeRequest) -> GradeRunResult:
        """Grade completed NBA spreads snapshot rows."""
