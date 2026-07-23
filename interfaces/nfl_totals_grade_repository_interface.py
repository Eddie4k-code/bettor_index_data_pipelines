"""ABC for append-only NFL totals grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NflTotalsGradeRecord


class NflTotalsGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NflTotalsGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
