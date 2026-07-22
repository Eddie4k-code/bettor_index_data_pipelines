"""Parametrized tests for explicit team-bet snapshot write repositories."""

import importlib
from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)


def _base_record_fields(**overrides):
    defaults = {
        "observation_time": OBSERVATION_TIME,
        "event_id": "evt-1",
        "bookmaker": "draftkings",
        "outcome_name": "Boston Celtics",
        "commence_time": datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc),
        "outcome_point": None,
        "outcome_price": -110.0,
        "market_last_update": datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
        "home_team": "Boston Celtics",
        "away_team": "Los Angeles Lakers",
        "hit_rate_market_last_update": datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc),
        "created_at": datetime(2026, 7, 21, 12, 5, tzinfo=timezone.utc),
    }
    defaults.update(overrides)
    return defaults


SNAPSHOT_REPO_CASES = [
    pytest.param(
        "repositories.team_bets.nba_spreads_snapshot_repository",
        "NbaSpreadsSnapshotRepository",
        "schemas.team_bets.NbaSpreadsSnapshotRecord",
        "db.models.owned.nba_team_bet_spreads_pregame_snapshots.NbaTeamBetSpreadsPregameSnapshot",
        "nba_spreads_v1",
        _base_record_fields(
            spread=-3.5,
            last_n_covers=6,
            last_n_sample=10,
            last_n_window=10,
            h2h_covers=2,
            h2h_sample=3,
            h2h_window=10,
            venue_covers=4,
            venue_sample=5,
            venue_window=10,
            venue_type="home",
            outcome_point=-3.5,
        ),
        id="nba_spreads",
    ),
    pytest.param(
        "repositories.team_bets.nba_totals_snapshot_repository",
        "NbaTotalsSnapshotRepository",
        "schemas.team_bets.NbaTotalsSnapshotRecord",
        "db.models.owned.nba_team_bet_totals_pregame_snapshots.NbaTeamBetTotalsPregameSnapshot",
        "nba_totals_v1",
        _base_record_fields(
            direction="Over",
            line=224.5,
            configured_window=10,
            home_team_clears=6,
            home_team_sample=10,
            away_team_clears=5,
            away_team_sample=10,
            h2h_window=10,
            h2h_sample=3,
            h2h_clears=2,
            h2h_avg_total=220.0,
            outcome_name="Over",
            outcome_point=224.5,
        ),
        id="nba_totals",
    ),
    pytest.param(
        "repositories.team_bets.mlb_h2h_snapshot_repository",
        "MlbH2hSnapshotRepository",
        "schemas.team_bets.MlbH2hSnapshotRecord",
        "db.models.owned.mlb_team_bet_h2h_pregame_snapshots.MlbTeamBetH2hPregameSnapshot",
        "mlb_h2h_v1",
        _base_record_fields(
            last_n_wins=7,
            last_n_losses=3,
            last_n_sample=10,
            last_n_window=10,
        ),
        id="mlb_h2h",
    ),
    pytest.param(
        "repositories.team_bets.mlb_spreads_snapshot_repository",
        "MlbSpreadsSnapshotRepository",
        "schemas.team_bets.MlbSpreadsSnapshotRecord",
        "db.models.owned.mlb_team_bet_spreads_pregame_snapshots.MlbTeamBetSpreadsPregameSnapshot",
        "mlb_spreads_v1",
        _base_record_fields(
            spread=-1.5,
            last_n_covers=6,
            last_n_sample=10,
            last_n_window=10,
            h2h_covers=2,
            h2h_sample=3,
            h2h_window=10,
            venue_covers=4,
            venue_sample=5,
            venue_window=10,
            venue_type="home",
            outcome_point=-1.5,
        ),
        id="mlb_spreads",
    ),
    pytest.param(
        "repositories.team_bets.mlb_totals_snapshot_repository",
        "MlbTotalsSnapshotRepository",
        "schemas.team_bets.MlbTotalsSnapshotRecord",
        "db.models.owned.mlb_team_bet_totals_pregame_snapshots.MlbTeamBetTotalsPregameSnapshot",
        "mlb_totals_v1",
        _base_record_fields(
            direction="Over",
            line=8.5,
            configured_window=10,
            home_team_clears=6,
            home_team_sample=10,
            away_team_clears=5,
            away_team_sample=10,
            h2h_window=10,
            h2h_sample=3,
            h2h_clears=2,
            outcome_name="Over",
            outcome_point=8.5,
        ),
        id="mlb_totals",
    ),
    pytest.param(
        "repositories.team_bets.nfl_h2h_snapshot_repository",
        "NflH2hSnapshotRepository",
        "schemas.team_bets.NflH2hSnapshotRecord",
        "db.models.owned.nfl_team_bet_h2h_pregame_snapshots.NflTeamBetH2hPregameSnapshot",
        "nfl_h2h_v1",
        _base_record_fields(
            last_n_wins=7,
            last_n_losses=3,
            last_n_sample=10,
            last_n_window=10,
        ),
        id="nfl_h2h",
    ),
    pytest.param(
        "repositories.team_bets.nfl_spreads_snapshot_repository",
        "NflSpreadsSnapshotRepository",
        "schemas.team_bets.NflSpreadsSnapshotRecord",
        "db.models.owned.nfl_team_bet_spreads_pregame_snapshots.NflTeamBetSpreadsPregameSnapshot",
        "nfl_spreads_v1",
        _base_record_fields(
            spread=-3.5,
            last_n_covers=6,
            last_n_sample=10,
            last_n_window=10,
            h2h_covers=2,
            h2h_sample=3,
            h2h_window=10,
            venue_covers=4,
            venue_sample=5,
            venue_window=10,
            venue_type="home",
            outcome_point=-3.5,
        ),
        id="nfl_spreads",
    ),
    pytest.param(
        "repositories.team_bets.nfl_totals_snapshot_repository",
        "NflTotalsSnapshotRepository",
        "schemas.team_bets.NflTotalsSnapshotRecord",
        "db.models.owned.nfl_team_bet_totals_pregame_snapshots.NflTeamBetTotalsPregameSnapshot",
        "nfl_totals_v1",
        _base_record_fields(
            direction="Over",
            line=44.5,
            configured_window=10,
            home_team_clears=6,
            home_team_sample=10,
            away_team_clears=5,
            away_team_sample=10,
            h2h_window=10,
            h2h_sample=3,
            h2h_clears=2,
            outcome_name="Over",
            outcome_point=44.5,
        ),
        id="nfl_totals",
    ),
    pytest.param(
        "repositories.team_bets.cfb_h2h_snapshot_repository",
        "CfbH2hSnapshotRepository",
        "schemas.team_bets.CfbH2hSnapshotRecord",
        "db.models.owned.cfb_team_bet_h2h_pregame_snapshots.CfbTeamBetH2hPregameSnapshot",
        "cfb_h2h_v1",
        _base_record_fields(
            last_n_wins=7,
            last_n_losses=3,
            last_n_sample=10,
            last_n_window=10,
        ),
        id="cfb_h2h",
    ),
    pytest.param(
        "repositories.team_bets.cfb_spreads_snapshot_repository",
        "CfbSpreadsSnapshotRepository",
        "schemas.team_bets.CfbSpreadsSnapshotRecord",
        "db.models.owned.cfb_team_bet_spreads_pregame_snapshots.CfbTeamBetSpreadsPregameSnapshot",
        "cfb_spreads_v1",
        _base_record_fields(
            spread=-7.0,
            last_n_covers=6,
            last_n_sample=10,
            last_n_window=10,
            h2h_covers=2,
            h2h_sample=3,
            h2h_window=10,
            venue_covers=4,
            venue_sample=5,
            venue_window=10,
            venue_type="home",
            outcome_point=-7.0,
        ),
        id="cfb_spreads",
    ),
    pytest.param(
        "repositories.team_bets.cfb_totals_snapshot_repository",
        "CfbTotalsSnapshotRepository",
        "schemas.team_bets.CfbTotalsSnapshotRecord",
        "db.models.owned.cfb_team_bet_totals_pregame_snapshots.CfbTeamBetTotalsPregameSnapshot",
        "cfb_totals_v1",
        _base_record_fields(
            direction="Over",
            line=52.5,
            configured_window=10,
            home_team_clears=6,
            home_team_sample=10,
            away_team_clears=5,
            away_team_sample=10,
            h2h_window=10,
            h2h_sample=3,
            h2h_clears=2,
            outcome_name="Over",
            outcome_point=52.5,
        ),
        id="cfb_totals",
    ),
]


def _import_symbol(dotted_path: str):
    module_path, _, symbol = dotted_path.rpartition(".")
    module = importlib.import_module(module_path)
    return getattr(module, symbol)


@pytest.mark.parametrize(
    "repo_path,repo_cls,record_path,orm_path,snapshot_version,record_fields",
    SNAPSHOT_REPO_CASES,
)
class TestTeamBetSnapshotRepositories:
    def test_insert_if_absent_returns_false_when_row_exists(
        self,
        repo_path,
        repo_cls,
        record_path,
        orm_path,
        snapshot_version,
        record_fields,
    ):
        repository_cls = _import_symbol(f"{repo_path}.{repo_cls}")
        record_cls = _import_symbol(record_path)

        db = MagicMock()
        db.query.return_value.filter_by.return_value.first.return_value = MagicMock()

        inserted = repository_cls(db).insert_if_absent(record_cls(**record_fields))

        assert inserted is False
        db.add.assert_not_called()

    def test_insert_if_absent_persists_new_row(
        self,
        repo_path,
        repo_cls,
        record_path,
        orm_path,
        snapshot_version,
        record_fields,
    ):
        repository_cls = _import_symbol(f"{repo_path}.{repo_cls}")
        record_cls = _import_symbol(record_path)
        orm_cls = _import_symbol(orm_path)

        db = MagicMock()
        db.query.return_value.filter_by.return_value.first.return_value = None

        inserted = repository_cls(db).insert_if_absent(record_cls(**record_fields))

        assert inserted is True
        db.add.assert_called_once()
        orm_row = db.add.call_args.args[0]
        assert isinstance(orm_row, orm_cls)
        assert orm_row.snapshot_version == snapshot_version
        db.commit.assert_called_once()
