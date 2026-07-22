"""Shared SQLAlchemy column mixins for team-bet pregame snapshot tables."""

from sqlalchemy import Column, DateTime, Float, Integer, String

TEAM_BET_SNAPSHOT_PK_COLUMNS: tuple[str, ...] = (
    "observation_time",
    "event_id",
    "bookmaker",
    "outcome_name",
    "snapshot_version",
)

TEAM_BET_SNAPSHOT_BASE_COLUMNS: tuple[str, ...] = (
    *TEAM_BET_SNAPSHOT_PK_COLUMNS,
    "sport_key",
    "market_key",
    "commence_time",
    "outcome_point",
    "outcome_price",
    "market_last_update",
    "home_team",
    "away_team",
    "home_team_id",
    "away_team_id",
    "outcome_team_id",
    "hit_rate_market_last_update",
    "created_at",
    "season",
)

TEAM_BET_H2H_FEATURE_COLUMNS: tuple[str, ...] = (
    "last_n_wins",
    "last_n_losses",
    "last_n_sample",
    "last_n_window",
    "venue_wins",
    "venue_losses",
    "venue_sample",
    "venue_window",
    "venue_type",
    "h2h_wins",
    "h2h_losses",
    "h2h_sample",
    "h2h_window",
)

TEAM_BET_SPREADS_FEATURE_COLUMNS: tuple[str, ...] = (
    "spread",
    "last_n_covers",
    "last_n_sample",
    "last_n_window",
    "h2h_covers",
    "h2h_sample",
    "h2h_window",
    "venue_covers",
    "venue_sample",
    "venue_window",
    "venue_type",
)

TEAM_BET_TOTALS_FEATURE_COLUMNS: tuple[str, ...] = (
    "direction",
    "line",
    "configured_window",
    "home_team_clears",
    "home_team_sample",
    "away_team_clears",
    "away_team_sample",
    "h2h_window",
    "h2h_sample",
    "h2h_clears",
    "h2h_avg_total",
)


class TeamBetSnapshotBaseColumns:
    """Identity, odds, and audit columns shared by all snapshot tables."""

    observation_time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    event_id = Column(String, primary_key=True, nullable=False)
    bookmaker = Column(String, primary_key=True, nullable=False)
    outcome_name = Column(String, primary_key=True, nullable=False)
    snapshot_version = Column(String, primary_key=True, nullable=False)
    sport_key = Column(String, nullable=False, index=True)
    market_key = Column(String, nullable=False, index=True)
    commence_time = Column(DateTime(timezone=True), nullable=False)
    outcome_point = Column(Float, nullable=True)
    outcome_price = Column(Float, nullable=False)
    market_last_update = Column(DateTime(timezone=True), nullable=False)
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    home_team_id = Column(Integer, nullable=True)
    away_team_id = Column(Integer, nullable=True)
    outcome_team_id = Column(Integer, nullable=True)
    hit_rate_market_last_update = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
    season = Column(Integer, nullable=True)


class TeamBetH2hFeatureColumns:
    """Moneyline W/L window columns copied from upstream hit-rate rows."""

    last_n_wins = Column(Integer, nullable=True)
    last_n_losses = Column(Integer, nullable=True)
    last_n_sample = Column(Integer, nullable=True)
    last_n_window = Column(Integer, nullable=True)
    venue_wins = Column(Integer, nullable=True)
    venue_losses = Column(Integer, nullable=True)
    venue_sample = Column(Integer, nullable=True)
    venue_window = Column(Integer, nullable=True)
    venue_type = Column(String, nullable=True)
    h2h_wins = Column(Integer, nullable=True)
    h2h_losses = Column(Integer, nullable=True)
    h2h_sample = Column(Integer, nullable=True)
    h2h_window = Column(Integer, nullable=True)


class TeamBetSpreadsFeatureColumns:
    """Spread cover window columns copied from upstream hit-rate rows."""

    spread = Column(Float, nullable=False)
    last_n_covers = Column(Integer, nullable=False)
    last_n_sample = Column(Integer, nullable=False)
    last_n_window = Column(Integer, nullable=False)
    h2h_covers = Column(Integer, nullable=False)
    h2h_sample = Column(Integer, nullable=False)
    h2h_window = Column(Integer, nullable=False)
    venue_covers = Column(Integer, nullable=False)
    venue_sample = Column(Integer, nullable=False)
    venue_window = Column(Integer, nullable=False)
    venue_type = Column(String, nullable=False)


class TeamBetTotalsFeatureColumns:
    """Totals clear window columns copied from upstream hit-rate rows."""

    direction = Column(String, nullable=False)
    line = Column(Float, nullable=False)
    configured_window = Column(Integer, nullable=False)
    home_team_clears = Column(Integer, nullable=False)
    home_team_sample = Column(Integer, nullable=False)
    away_team_clears = Column(Integer, nullable=False)
    away_team_sample = Column(Integer, nullable=False)
    h2h_window = Column(Integer, nullable=False)
    h2h_sample = Column(Integer, nullable=False)
    h2h_clears = Column(Integer, nullable=False)
    h2h_avg_total = Column(Float, nullable=True)
