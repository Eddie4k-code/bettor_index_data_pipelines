"""Tests for explicit team-bet snapshot record classes (12 sport/market types)."""

import pytest

from schemas.team_bets import (
    CfbH2hSnapshotRecord,
    CfbSpreadsSnapshotRecord,
    CfbTotalsSnapshotRecord,
    MlbH2hSnapshotRecord,
    MlbSpreadsSnapshotRecord,
    MlbTotalsSnapshotRecord,
    NbaH2hSnapshotRecord,
    NbaSpreadsSnapshotRecord,
    NbaTotalsSnapshotRecord,
    NflH2hSnapshotRecord,
    NflSpreadsSnapshotRecord,
    NflTotalsSnapshotRecord,
)


RECORD_CONSTANTS = [
    pytest.param(
        NbaH2hSnapshotRecord,
        "basketball_nba",
        "h2h",
        "nba_h2h_v1",
        id="nba_h2h",
    ),
    pytest.param(
        NbaSpreadsSnapshotRecord,
        "basketball_nba",
        "spreads",
        "nba_spreads_v1",
        id="nba_spreads",
    ),
    pytest.param(
        NbaTotalsSnapshotRecord,
        "basketball_nba",
        "totals",
        "nba_totals_v1",
        id="nba_totals",
    ),
    pytest.param(
        MlbH2hSnapshotRecord,
        "baseball_mlb",
        "h2h",
        "mlb_h2h_v1",
        id="mlb_h2h",
    ),
    pytest.param(
        MlbSpreadsSnapshotRecord,
        "baseball_mlb",
        "spreads",
        "mlb_spreads_v1",
        id="mlb_spreads",
    ),
    pytest.param(
        MlbTotalsSnapshotRecord,
        "baseball_mlb",
        "totals",
        "mlb_totals_v1",
        id="mlb_totals",
    ),
    pytest.param(
        NflH2hSnapshotRecord,
        "americanfootball_nfl",
        "h2h",
        "nfl_h2h_v1",
        id="nfl_h2h",
    ),
    pytest.param(
        NflSpreadsSnapshotRecord,
        "americanfootball_nfl",
        "spreads",
        "nfl_spreads_v1",
        id="nfl_spreads",
    ),
    pytest.param(
        NflTotalsSnapshotRecord,
        "americanfootball_nfl",
        "totals",
        "nfl_totals_v1",
        id="nfl_totals",
    ),
    pytest.param(
        CfbH2hSnapshotRecord,
        "americanfootball_ncaaf",
        "h2h",
        "cfb_h2h_v1",
        id="cfb_h2h",
    ),
    pytest.param(
        CfbSpreadsSnapshotRecord,
        "americanfootball_ncaaf",
        "spreads",
        "cfb_spreads_v1",
        id="cfb_spreads",
    ),
    pytest.param(
        CfbTotalsSnapshotRecord,
        "americanfootball_ncaaf",
        "totals",
        "cfb_totals_v1",
        id="cfb_totals",
    ),
]


@pytest.mark.parametrize(
    ("record_cls", "sport_key", "market_key", "snapshot_version"),
    RECORD_CONSTANTS,
)
def test_snapshot_record_has_fixed_identity_defaults(
    record_cls,
    sport_key,
    market_key,
    snapshot_version,
):
    assert record_cls.model_fields["sport_key"].default == sport_key
    assert record_cls.model_fields["market_key"].default == market_key
    assert record_cls.model_fields["snapshot_version"].default == snapshot_version
