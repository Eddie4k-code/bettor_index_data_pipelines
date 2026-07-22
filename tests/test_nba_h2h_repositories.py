"""Unit tests for NBA H2H snapshot read/write repositories (mocked SQLAlchemy session)."""

from datetime import datetime, timezone
from unittest.mock import MagicMock

from db.models.owned.nba_team_bet_h2h_pregame_snapshots import NbaTeamBetH2hPregameSnapshot
from db.models.upstream.nba_team_bet_hit_rates import NbaTeamBetHitRates
from db.models.upstream.odds_api_featured_odds import OddsAPIFeaturedOdds
from repositories.featured_odds_read_repository import FeaturedOddsReadRepository
from repositories.team_bets.nba_h2h_hit_rate_read_repository import NbaH2hHitRateReadRepository
from repositories.team_bets.nba_h2h_snapshot_repository import NbaH2hSnapshotRepository
from schemas.team_bets import NbaH2hSnapshotRecord

OBSERVATION_TIME = datetime(2026, 7, 21, 12, 0, tzinfo=timezone.utc)


def _snapshot_record(**overrides) -> NbaH2hSnapshotRecord:
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
        "last_n_wins": 7,
        "last_n_losses": 3,
        "last_n_sample": 10,
        "last_n_window": 10,
    }
    defaults.update(overrides)
    return NbaH2hSnapshotRecord(**defaults)


class TestFeaturedOddsReadRepository:
    def test_maps_orm_row_to_dto(self):
        db = MagicMock()
        orm_row = OddsAPIFeaturedOdds(
            event_id="evt-1",
            bookmaker="draftkings",
            market_key="h2h",
            outcome_name="Boston Celtics",
            sport_key="basketball_nba",
            commence_time=datetime(2026, 7, 21, 23, 0, tzinfo=timezone.utc),
            outcome_price=-110.0,
            outcome_point=None,
            market_last_update=datetime(2026, 7, 21, 11, 30, tzinfo=timezone.utc),
            home_team="Boston Celtics",
            away_team="Los Angeles Lakers",
        )
        db.query.return_value.filter.return_value.all.return_value = [orm_row]

        rows = FeaturedOddsReadRepository(db).fetch_pregame_odds(
            sport_key="basketball_nba",
            market_key="h2h",
            observation_time=OBSERVATION_TIME,
        )

        assert len(rows) == 1
        assert rows[0].event_id == "evt-1"
        assert rows[0].sport_key == "basketball_nba"


class TestNbaH2hHitRateReadRepository:
    def test_maps_string_datetimes_to_dto(self):
        db = MagicMock()
        orm_row = NbaTeamBetHitRates(
            event_id="evt-1",
            bookmaker="draftkings",
            market_key="h2h",
            outcome_name="Boston Celtics",
            commence_time="2026-07-21T23:00:00+00:00",
            outcome_price="-110",
            home_team="Boston Celtics",
            away_team="Los Angeles Lakers",
            home_team_id=1,
            away_team_id=2,
            outcome_team_id=1,
            market_last_update="2026-07-21T11:00:00+00:00",
            sport_key="basketball_nba",
            last_n_wins=7,
            last_n_losses=3,
            last_n_sample=10,
            last_n_window=10,
        )
        db.query.return_value.filter.return_value.all.return_value = [orm_row]

        rows = NbaH2hHitRateReadRepository(db).fetch_pregame_hit_rates(
            observation_time=OBSERVATION_TIME,
        )

        assert len(rows) == 1
        assert rows[0].market_last_update == datetime(2026, 7, 21, 11, 0, tzinfo=timezone.utc)
        assert rows[0].last_n_wins == 7

    def test_excludes_rows_after_observation_time(self):
        db = MagicMock()
        late_row = NbaTeamBetHitRates(
            event_id="evt-late",
            bookmaker="draftkings",
            market_key="h2h",
            outcome_name="Boston Celtics",
            commence_time="2026-07-21T23:00:00+00:00",
            outcome_price="-110",
            home_team="Boston Celtics",
            away_team="Los Angeles Lakers",
            market_last_update="2026-07-21T12:01:00+00:00",
            sport_key="basketball_nba",
        )
        db.query.return_value.filter.return_value.all.return_value = [late_row]

        rows = NbaH2hHitRateReadRepository(db).fetch_pregame_hit_rates(
            observation_time=OBSERVATION_TIME,
        )

        assert rows == []


class TestNbaH2hSnapshotRepository:
    def test_insert_if_absent_returns_false_when_row_exists(self):
        db = MagicMock()
        db.query.return_value.filter_by.return_value.first.return_value = MagicMock()

        inserted = NbaH2hSnapshotRepository(db).insert_if_absent(_snapshot_record())

        assert inserted is False
        db.add.assert_not_called()

    def test_insert_if_absent_persists_new_row(self):
        db = MagicMock()
        db.query.return_value.filter_by.return_value.first.return_value = None

        inserted = NbaH2hSnapshotRepository(db).insert_if_absent(_snapshot_record())

        assert inserted is True
        db.add.assert_called_once()
        orm_row = db.add.call_args.args[0]
        assert isinstance(orm_row, NbaTeamBetH2hPregameSnapshot)
        assert orm_row.snapshot_version == "nba_h2h_v1"
        db.commit.assert_called_once()
