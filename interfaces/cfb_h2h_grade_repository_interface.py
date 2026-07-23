"""ABC for append-only CFB H2H grade persistence."""

from abc import ABC, abstractmethod

from schemas.team_bets import CfbH2hGradeRecord


class CfbH2hGradeRepositoryInterface(ABC):
    @abstractmethod
    def insert_if_absent(self, record: CfbH2hGradeRecord) -> bool:
        """Insert the grade when PK is absent; return False when it already exists."""
