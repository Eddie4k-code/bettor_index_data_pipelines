"""ABC for the CFB H2H grade orchestrator."""

from abc import ABC, abstractmethod

from schemas.grade import GradeRequest, GradeRunResult


class CfbH2hGradePipelineInterface(ABC):
    @abstractmethod
    def run(self, request: GradeRequest) -> GradeRunResult:
        """Grade completed CFB H2H snapshot rows."""
