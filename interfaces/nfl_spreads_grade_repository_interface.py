"""ABC for append-only NFL spreads grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NflSpreadsGradeRecord


class NflSpreadsGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NflSpreadsGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
