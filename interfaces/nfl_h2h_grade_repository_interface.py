"""ABC for append-only NFL H2H grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NflH2hGradeRecord


class NflH2hGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NflH2hGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
