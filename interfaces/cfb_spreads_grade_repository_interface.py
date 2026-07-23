"""ABC for append-only CFB spreads grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import CfbSpreadsGradeRecord


class CfbSpreadsGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: CfbSpreadsGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
