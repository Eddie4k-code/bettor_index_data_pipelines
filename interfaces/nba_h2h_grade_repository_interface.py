"""ABC for append-only NBA H2H grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NbaH2hGradeRecord


class NbaH2hGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NbaH2hGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
