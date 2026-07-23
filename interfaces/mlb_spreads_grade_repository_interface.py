"""ABC for append-only MLB spreads grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import MlbSpreadsGradeRecord


class MlbSpreadsGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: MlbSpreadsGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
