"""ABC for append-only CFB totals grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import CfbTotalsGradeRecord


class CfbTotalsGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: CfbTotalsGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
