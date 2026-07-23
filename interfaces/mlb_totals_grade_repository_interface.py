"""ABC for append-only MLB totals grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import MlbTotalsGradeRecord


class MlbTotalsGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: MlbTotalsGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
