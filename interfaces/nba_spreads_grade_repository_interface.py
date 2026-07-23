"""ABC for append-only NBA spreads grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import NbaSpreadsGradeRecord


class NbaSpreadsGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: NbaSpreadsGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
