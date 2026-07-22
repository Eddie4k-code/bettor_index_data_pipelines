"""Point-in-time reads from ``nba_team_bet_hit_rates``."""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from db.models.upstream.nba_team_bet_hit_rates import NbaTeamBetHitRates
from interfaces.nba_h2h_hit_rate_read_repository_interface import NbaH2hHitRateReadRepositoryInterface
from schemas.snapshot import ALLOWED_BOOKMAKERS
from schemas.team_bets.upstream_rows import TeamBetH2hHitRateRow


class NbaH2hHitRateReadRepository(NbaH2hHitRateReadRepositoryInterface):
    def __init__(self, db: Session):
        self.db = db

    def fetch_pregame_hit_rates(
        self,
        *,
        observation_time: datetime,
    ) -> list[TeamBetH2hHitRateRow]:
        rows = (
            self.db.query(NbaTeamBetHitRates)
            .filter(
                NbaTeamBetHitRates.market_key == "h2h",
                NbaTeamBetHitRates.bookmaker.in_(ALLOWED_BOOKMAKERS),
            )
            .all()
        )
        return [
            dto
            for row in rows
            if (dto := self._to_row(row)) is not None
            and dto.market_last_update <= observation_time
            and self._parse_datetime(row.commence_time) > observation_time
        ]

    @staticmethod
    def _parse_datetime(value: datetime | str) -> datetime:
        if isinstance(value, datetime):
            return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
        if isinstance(value, str):
            normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
            parsed = datetime.fromisoformat(normalized)
            return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)
        raise ValueError(f"Cannot parse datetime from {value!r}")

    def _to_row(self, row: NbaTeamBetHitRates) -> TeamBetH2hHitRateRow:
        return TeamBetH2hHitRateRow(
            event_id=row.event_id,
            bookmaker=row.bookmaker,
            market_key=row.market_key,
            outcome_name=row.outcome_name,
            market_last_update=self._parse_datetime(row.market_last_update),
            home_team=row.home_team,
            away_team=row.away_team,
            home_team_id=row.home_team_id,
            away_team_id=row.away_team_id,
            outcome_team_id=row.outcome_team_id,
            last_n_wins=row.last_n_wins,
            last_n_losses=row.last_n_losses,
            last_n_sample=row.last_n_sample,
            last_n_window=row.last_n_window,
            venue_wins=row.venue_wins,
            venue_losses=row.venue_losses,
            venue_sample=row.venue_sample,
            venue_window=row.venue_window,
            venue_type=row.venue_type,
            h2h_wins=row.h2h_wins,
            h2h_losses=row.h2h_losses,
            h2h_sample=row.h2h_sample,
            h2h_window=row.h2h_window,
        )
