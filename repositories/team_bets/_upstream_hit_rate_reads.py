"""Shared point-in-time helpers for upstream team-bet hit-rate read repositories."""

from datetime import datetime, timezone

from schemas.team_bets.upstream_rows import (
    TeamBetH2hHitRateRow,
    TeamBetSpreadsHitRateRow,
    TeamBetTotalsHitRateRow,
)


def parse_datetime(value: datetime | str) -> datetime:
    if isinstance(value, datetime):
        return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)
    if isinstance(value, str):
        normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
        parsed = datetime.fromisoformat(normalized)
        return parsed if parsed.tzinfo is not None else parsed.replace(tzinfo=timezone.utc)
    raise ValueError(f"Cannot parse datetime from {value!r}")


def is_observable_at_observation_time(row, observation_time: datetime) -> bool:
    market_last_update = parse_datetime(row.market_last_update)
    commence_time = parse_datetime(row.commence_time)
    return market_last_update <= observation_time and commence_time > observation_time


def map_h2h_hit_rate_row(row) -> TeamBetH2hHitRateRow | None:
    return TeamBetH2hHitRateRow(
        event_id=row.event_id,
        bookmaker=row.bookmaker,
        market_key=row.market_key,
        outcome_name=row.outcome_name,
        market_last_update=parse_datetime(row.market_last_update),
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


def map_spreads_hit_rate_row(row) -> TeamBetSpreadsHitRateRow | None:
    return TeamBetSpreadsHitRateRow(
        event_id=row.event_id,
        bookmaker=row.bookmaker,
        market_key=row.market_key,
        outcome_name=row.outcome_name,
        market_last_update=parse_datetime(row.market_last_update),
        home_team=row.home_team,
        away_team=row.away_team,
        home_team_id=row.home_team_id,
        away_team_id=row.away_team_id,
        outcome_team_id=row.outcome_team_id,
        spread=row.spread,
        last_n_covers=row.last_n_covers,
        last_n_sample=row.last_n_sample,
        last_n_window=row.last_n_window,
        h2h_covers=row.h2h_covers,
        h2h_sample=row.h2h_sample,
        h2h_window=row.h2h_window,
        venue_covers=row.venue_covers,
        venue_sample=row.venue_sample,
        venue_window=row.venue_window,
        venue_type=row.venue_type,
    )


def map_totals_hit_rate_row(row) -> TeamBetTotalsHitRateRow | None:
    return TeamBetTotalsHitRateRow(
        event_id=row.event_id,
        bookmaker=row.bookmaker,
        market_key=row.market_key,
        outcome_name=row.outcome_name,
        market_last_update=parse_datetime(row.market_last_update),
        home_team=row.home_team,
        away_team=row.away_team,
        home_team_id=row.home_team_id,
        away_team_id=row.away_team_id,
        direction=row.direction,
        line=row.line,
        configured_window=row.configured_window,
        home_team_clears=row.home_team_clears,
        home_team_sample=row.home_team_sample,
        away_team_clears=row.away_team_clears,
        away_team_sample=row.away_team_sample,
        h2h_window=row.h2h_window,
        h2h_sample=row.h2h_sample,
        h2h_clears=row.h2h_clears,
        h2h_avg_total=row.h2h_avg_total,
    )
