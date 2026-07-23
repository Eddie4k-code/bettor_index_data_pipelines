"""ABC for append-only MLB H2H grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import MlbH2hGradeRecord


class MlbH2hGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: MlbH2hGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
