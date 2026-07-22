"""Tests for owned team-bet pregame snapshot SQLAlchemy models."""

import pytest
from sqlalchemy import create_engine, inspect

from db.db import create_owned_tables
from db.models import owned
from db.models.owned.mixins import (
    TEAM_BET_SNAPSHOT_BASE_COLUMNS,
    TEAM_BET_SNAPSHOT_PK_COLUMNS,
    TEAM_BET_H2H_FEATURE_COLUMNS,
    TEAM_BET_SPREADS_FEATURE_COLUMNS,
    TEAM_BET_TOTALS_FEATURE_COLUMNS,
)
from db.models.owned.cfb_team_bet_h2h_pregame_snapshots import CfbTeamBetH2hPregameSnapshot
from db.models.owned.cfb_team_bet_spreads_pregame_snapshots import CfbTeamBetSpreadsPregameSnapshot
from db.models.owned.cfb_team_bet_totals_pregame_snapshots import CfbTeamBetTotalsPregameSnapshot
from db.models.owned.mlb_team_bet_h2h_pregame_snapshots import MlbTeamBetH2hPregameSnapshot
from db.models.owned.mlb_team_bet_spreads_pregame_snapshots import MlbTeamBetSpreadsPregameSnapshot
from db.models.owned.mlb_team_bet_totals_pregame_snapshots import MlbTeamBetTotalsPregameSnapshot
from db.models.owned.nba_team_bet_h2h_pregame_snapshots import NbaTeamBetH2hPregameSnapshot
from db.models.owned.nba_team_bet_spreads_pregame_snapshots import NbaTeamBetSpreadsPregameSnapshot
from db.models.owned.nba_team_bet_totals_pregame_snapshots import NbaTeamBetTotalsPregameSnapshot
from db.models.owned.nfl_team_bet_h2h_pregame_snapshots import NflTeamBetH2hPregameSnapshot
from db.models.owned.nfl_team_bet_spreads_pregame_snapshots import NflTeamBetSpreadsPregameSnapshot
from db.models.owned.nfl_team_bet_totals_pregame_snapshots import NflTeamBetTotalsPregameSnapshot

OWNED_SNAPSHOT_TABLES = {
    NbaTeamBetH2hPregameSnapshot: "nba_team_bet_h2h_pregame_snapshots",
    NbaTeamBetSpreadsPregameSnapshot: "nba_team_bet_spreads_pregame_snapshots",
    NbaTeamBetTotalsPregameSnapshot: "nba_team_bet_totals_pregame_snapshots",
    MlbTeamBetH2hPregameSnapshot: "mlb_team_bet_h2h_pregame_snapshots",
    MlbTeamBetSpreadsPregameSnapshot: "mlb_team_bet_spreads_pregame_snapshots",
    MlbTeamBetTotalsPregameSnapshot: "mlb_team_bet_totals_pregame_snapshots",
    NflTeamBetH2hPregameSnapshot: "nfl_team_bet_h2h_pregame_snapshots",
    NflTeamBetSpreadsPregameSnapshot: "nfl_team_bet_spreads_pregame_snapshots",
    NflTeamBetTotalsPregameSnapshot: "nfl_team_bet_totals_pregame_snapshots",
    CfbTeamBetH2hPregameSnapshot: "cfb_team_bet_h2h_pregame_snapshots",
    CfbTeamBetSpreadsPregameSnapshot: "cfb_team_bet_spreads_pregame_snapshots",
    CfbTeamBetTotalsPregameSnapshot: "cfb_team_bet_totals_pregame_snapshots",
}

OWNED_SNAPSHOT_MODELS = [
    pytest.param(
        NbaTeamBetH2hPregameSnapshot,
        "nba_team_bet_h2h_pregame_snapshots",
        TEAM_BET_H2H_FEATURE_COLUMNS,
        id="nba_h2h",
    ),
    pytest.param(
        NbaTeamBetSpreadsPregameSnapshot,
        "nba_team_bet_spreads_pregame_snapshots",
        TEAM_BET_SPREADS_FEATURE_COLUMNS,
        id="nba_spreads",
    ),
    pytest.param(
        NbaTeamBetTotalsPregameSnapshot,
        "nba_team_bet_totals_pregame_snapshots",
        TEAM_BET_TOTALS_FEATURE_COLUMNS,
        id="nba_totals",
    ),
    pytest.param(
        MlbTeamBetH2hPregameSnapshot,
        "mlb_team_bet_h2h_pregame_snapshots",
        TEAM_BET_H2H_FEATURE_COLUMNS,
        id="mlb_h2h",
    ),
    pytest.param(
        MlbTeamBetSpreadsPregameSnapshot,
        "mlb_team_bet_spreads_pregame_snapshots",
        TEAM_BET_SPREADS_FEATURE_COLUMNS,
        id="mlb_spreads",
    ),
    pytest.param(
        MlbTeamBetTotalsPregameSnapshot,
        "mlb_team_bet_totals_pregame_snapshots",
        TEAM_BET_TOTALS_FEATURE_COLUMNS,
        id="mlb_totals",
    ),
    pytest.param(
        NflTeamBetH2hPregameSnapshot,
        "nfl_team_bet_h2h_pregame_snapshots",
        TEAM_BET_H2H_FEATURE_COLUMNS,
        id="nfl_h2h",
    ),
    pytest.param(
        NflTeamBetSpreadsPregameSnapshot,
        "nfl_team_bet_spreads_pregame_snapshots",
        TEAM_BET_SPREADS_FEATURE_COLUMNS,
        id="nfl_spreads",
    ),
    pytest.param(
        NflTeamBetTotalsPregameSnapshot,
        "nfl_team_bet_totals_pregame_snapshots",
        TEAM_BET_TOTALS_FEATURE_COLUMNS,
        id="nfl_totals",
    ),
    pytest.param(
        CfbTeamBetH2hPregameSnapshot,
        "cfb_team_bet_h2h_pregame_snapshots",
        TEAM_BET_H2H_FEATURE_COLUMNS,
        id="cfb_h2h",
    ),
    pytest.param(
        CfbTeamBetSpreadsPregameSnapshot,
        "cfb_team_bet_spreads_pregame_snapshots",
        TEAM_BET_SPREADS_FEATURE_COLUMNS,
        id="cfb_spreads",
    ),
    pytest.param(
        CfbTeamBetTotalsPregameSnapshot,
        "cfb_team_bet_totals_pregame_snapshots",
        TEAM_BET_TOTALS_FEATURE_COLUMNS,
        id="cfb_totals",
    ),
]


def test_owned_models_registry_has_twelve_models():
    assert len(owned.OWNED_MODELS) == 12
    assert set(owned.OWNED_MODELS) == set(OWNED_SNAPSHOT_TABLES)


@pytest.mark.parametrize(("model_cls", "table_name", "feature_columns"), OWNED_SNAPSHOT_MODELS)
def test_model_table_name(model_cls, table_name, feature_columns):
    assert model_cls.__tablename__ == table_name


@pytest.mark.parametrize(("model_cls", "table_name", "feature_columns"), OWNED_SNAPSHOT_MODELS)
def test_model_primary_key_columns(model_cls, table_name, feature_columns):
    pk_columns = {column.name for column in model_cls.__table__.primary_key.columns}
    assert pk_columns == set(TEAM_BET_SNAPSHOT_PK_COLUMNS)


@pytest.mark.parametrize(("model_cls", "table_name", "feature_columns"), OWNED_SNAPSHOT_MODELS)
def test_model_has_shared_base_columns(model_cls, table_name, feature_columns):
    column_names = {column.name for column in model_cls.__table__.columns}
    assert set(TEAM_BET_SNAPSHOT_BASE_COLUMNS).issubset(column_names)


@pytest.mark.parametrize(("model_cls", "table_name", "feature_columns"), OWNED_SNAPSHOT_MODELS)
def test_model_has_market_feature_columns(model_cls, table_name, feature_columns):
    column_names = {column.name for column in model_cls.__table__.columns}
    assert set(feature_columns).issubset(column_names)


def test_create_owned_tables_materializes_all_snapshot_tables():
    engine = create_engine("sqlite:///:memory:")
    create_owned_tables(engine)

    inspector = inspect(engine)
    assert set(inspector.get_table_names()) == set(OWNED_SNAPSHOT_TABLES.values())
