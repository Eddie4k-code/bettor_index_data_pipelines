"""ABC for append-only NBA totals grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NbaTotalsGradeRecord


class NbaTotalsGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NbaTotalsGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
