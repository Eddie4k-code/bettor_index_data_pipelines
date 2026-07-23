"""CLI entrypoint for team-bet snapshot, grade, and export pipelines."""

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from db.db import ensure_owned_tables, get_db
from pipelines.team_bets.cfb_h2h_grade_pipeline import CfbH2hGradePipeline
from pipelines.team_bets.cfb_h2h_snapshot_pipeline import CfbH2hSnapshotPipeline
from pipelines.team_bets.cfb_spreads_grade_pipeline import CfbSpreadsGradePipeline
from pipelines.team_bets.cfb_spreads_snapshot_pipeline import CfbSpreadsSnapshotPipeline
from pipelines.team_bets.cfb_totals_grade_pipeline import CfbTotalsGradePipeline
from pipelines.team_bets.cfb_totals_snapshot_pipeline import CfbTotalsSnapshotPipeline
from pipelines.team_bets.mlb_h2h_grade_pipeline import MlbH2hGradePipeline
from pipelines.team_bets.mlb_h2h_snapshot_pipeline import MlbH2hSnapshotPipeline
from pipelines.team_bets.mlb_spreads_grade_pipeline import MlbSpreadsGradePipeline
from pipelines.team_bets.mlb_spreads_snapshot_pipeline import MlbSpreadsSnapshotPipeline
from pipelines.team_bets.mlb_totals_grade_pipeline import MlbTotalsGradePipeline
from pipelines.team_bets.mlb_totals_snapshot_pipeline import MlbTotalsSnapshotPipeline
from pipelines.team_bets.nba_h2h_grade_pipeline import NbaH2hGradePipeline
from pipelines.team_bets.nba_h2h_snapshot_pipeline import NbaH2hSnapshotPipeline
from pipelines.team_bets.nba_spreads_grade_pipeline import NbaSpreadsGradePipeline
from pipelines.team_bets.nba_spreads_snapshot_pipeline import NbaSpreadsSnapshotPipeline
from pipelines.team_bets.nba_totals_grade_pipeline import NbaTotalsGradePipeline
from pipelines.team_bets.nba_totals_snapshot_pipeline import NbaTotalsSnapshotPipeline
from pipelines.team_bets.nfl_h2h_grade_pipeline import NflH2hGradePipeline
from pipelines.team_bets.nfl_h2h_snapshot_pipeline import NflH2hSnapshotPipeline
from pipelines.team_bets.nfl_spreads_grade_pipeline import NflSpreadsGradePipeline
from pipelines.team_bets.nfl_spreads_snapshot_pipeline import NflSpreadsSnapshotPipeline
from pipelines.team_bets.nfl_totals_grade_pipeline import NflTotalsGradePipeline
from pipelines.team_bets.nfl_totals_snapshot_pipeline import NflTotalsSnapshotPipeline
from repositories.featured_odds_read_repository import FeaturedOddsReadRepository
from repositories.games_read_repository import GamesReadRepository
from repositories.team_bets.cfb_h2h_grade_repository import CfbH2hGradeRepository
from repositories.team_bets.cfb_h2h_hit_rate_read_repository import CfbH2hHitRateReadRepository
from repositories.team_bets.cfb_h2h_snapshot_read_repository import CfbH2hSnapshotReadRepository
from repositories.team_bets.cfb_h2h_snapshot_repository import CfbH2hSnapshotRepository
from repositories.team_bets.cfb_spreads_grade_repository import CfbSpreadsGradeRepository
from repositories.team_bets.cfb_spreads_hit_rate_read_repository import CfbSpreadsHitRateReadRepository
from repositories.team_bets.cfb_spreads_snapshot_read_repository import CfbSpreadsSnapshotReadRepository
from repositories.team_bets.cfb_spreads_snapshot_repository import CfbSpreadsSnapshotRepository
from repositories.team_bets.cfb_totals_grade_repository import CfbTotalsGradeRepository
from repositories.team_bets.cfb_totals_hit_rate_read_repository import CfbTotalsHitRateReadRepository
from repositories.team_bets.cfb_totals_snapshot_read_repository import CfbTotalsSnapshotReadRepository
from repositories.team_bets.cfb_totals_snapshot_repository import CfbTotalsSnapshotRepository
from repositories.team_bets.mlb_h2h_grade_repository import MlbH2hGradeRepository
from repositories.team_bets.mlb_h2h_hit_rate_read_repository import MlbH2hHitRateReadRepository
from repositories.team_bets.mlb_h2h_snapshot_read_repository import MlbH2hSnapshotReadRepository
from repositories.team_bets.mlb_h2h_snapshot_repository import MlbH2hSnapshotRepository
from repositories.team_bets.mlb_spreads_grade_repository import MlbSpreadsGradeRepository
from repositories.team_bets.mlb_spreads_hit_rate_read_repository import MlbSpreadsHitRateReadRepository
from repositories.team_bets.mlb_spreads_snapshot_read_repository import MlbSpreadsSnapshotReadRepository
from repositories.team_bets.mlb_spreads_snapshot_repository import MlbSpreadsSnapshotRepository
from repositories.team_bets.mlb_totals_grade_repository import MlbTotalsGradeRepository
from repositories.team_bets.mlb_totals_hit_rate_read_repository import MlbTotalsHitRateReadRepository
from repositories.team_bets.mlb_totals_snapshot_read_repository import MlbTotalsSnapshotReadRepository
from repositories.team_bets.mlb_totals_snapshot_repository import MlbTotalsSnapshotRepository
from repositories.team_bets.nba_h2h_grade_repository import NbaH2hGradeRepository
from repositories.team_bets.nba_h2h_hit_rate_read_repository import NbaH2hHitRateReadRepository
from repositories.team_bets.nba_h2h_snapshot_read_repository import NbaH2hSnapshotReadRepository
from repositories.team_bets.nba_h2h_snapshot_repository import NbaH2hSnapshotRepository
from repositories.team_bets.nba_spreads_grade_repository import NbaSpreadsGradeRepository
from repositories.team_bets.nba_spreads_hit_rate_read_repository import NbaSpreadsHitRateReadRepository
from repositories.team_bets.nba_spreads_snapshot_read_repository import NbaSpreadsSnapshotReadRepository
from repositories.team_bets.nba_spreads_snapshot_repository import NbaSpreadsSnapshotRepository
from repositories.team_bets.nba_totals_grade_repository import NbaTotalsGradeRepository
from repositories.team_bets.nba_totals_hit_rate_read_repository import NbaTotalsHitRateReadRepository
from repositories.team_bets.nba_totals_snapshot_read_repository import NbaTotalsSnapshotReadRepository
from repositories.team_bets.nba_totals_snapshot_repository import NbaTotalsSnapshotRepository
from repositories.team_bets.nfl_h2h_grade_repository import NflH2hGradeRepository
from repositories.team_bets.nfl_h2h_hit_rate_read_repository import NflH2hHitRateReadRepository
from repositories.team_bets.nfl_h2h_snapshot_read_repository import NflH2hSnapshotReadRepository
from repositories.team_bets.nfl_h2h_snapshot_repository import NflH2hSnapshotRepository
from repositories.team_bets.nfl_spreads_grade_repository import NflSpreadsGradeRepository
from repositories.team_bets.nfl_spreads_hit_rate_read_repository import NflSpreadsHitRateReadRepository
from repositories.team_bets.nfl_spreads_snapshot_read_repository import NflSpreadsSnapshotReadRepository
from repositories.team_bets.nfl_spreads_snapshot_repository import NflSpreadsSnapshotRepository
from repositories.team_bets.nfl_totals_grade_repository import NflTotalsGradeRepository
from repositories.team_bets.nfl_totals_hit_rate_read_repository import NflTotalsHitRateReadRepository
from repositories.team_bets.nfl_totals_snapshot_read_repository import NflTotalsSnapshotReadRepository
from repositories.team_bets.nfl_totals_snapshot_repository import NflTotalsSnapshotRepository
from schemas.grade import GradeRequest, GradeRunResult
from schemas.snapshot import SnapshotRequest, SnapshotRunResult

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SnapshotSpec:
    sport_key: str
    market_key: str
    pipeline_cls: Callable[..., Any]
    hit_rate_repo_cls: Callable[..., Any]
    snapshot_repo_cls: Callable[..., Any]


@dataclass(frozen=True)
class GradeSpec:
    sport_key: str
    market_key: str
    pipeline_cls: Callable[..., Any]
    snapshot_read_repo_cls: Callable[..., Any]
    grade_repo_cls: Callable[..., Any]


SNAPSHOT_SPECS: dict[str, SnapshotSpec] = {
    "nba-h2h": SnapshotSpec(
        sport_key="basketball_nba",
        market_key="h2h",
        pipeline_cls=NbaH2hSnapshotPipeline,
        hit_rate_repo_cls=NbaH2hHitRateReadRepository,
        snapshot_repo_cls=NbaH2hSnapshotRepository,
    ),
    "nba-spreads": SnapshotSpec(
        sport_key="basketball_nba",
        market_key="spreads",
        pipeline_cls=NbaSpreadsSnapshotPipeline,
        hit_rate_repo_cls=NbaSpreadsHitRateReadRepository,
        snapshot_repo_cls=NbaSpreadsSnapshotRepository,
    ),
    "nba-totals": SnapshotSpec(
        sport_key="basketball_nba",
        market_key="totals",
        pipeline_cls=NbaTotalsSnapshotPipeline,
        hit_rate_repo_cls=NbaTotalsHitRateReadRepository,
        snapshot_repo_cls=NbaTotalsSnapshotRepository,
    ),
    "mlb-h2h": SnapshotSpec(
        sport_key="baseball_mlb",
        market_key="h2h",
        pipeline_cls=MlbH2hSnapshotPipeline,
        hit_rate_repo_cls=MlbH2hHitRateReadRepository,
        snapshot_repo_cls=MlbH2hSnapshotRepository,
    ),
    "mlb-spreads": SnapshotSpec(
        sport_key="baseball_mlb",
        market_key="spreads",
        pipeline_cls=MlbSpreadsSnapshotPipeline,
        hit_rate_repo_cls=MlbSpreadsHitRateReadRepository,
        snapshot_repo_cls=MlbSpreadsSnapshotRepository,
    ),
    "mlb-totals": SnapshotSpec(
        sport_key="baseball_mlb",
        market_key="totals",
        pipeline_cls=MlbTotalsSnapshotPipeline,
        hit_rate_repo_cls=MlbTotalsHitRateReadRepository,
        snapshot_repo_cls=MlbTotalsSnapshotRepository,
    ),
    "nfl-h2h": SnapshotSpec(
        sport_key="americanfootball_nfl",
        market_key="h2h",
        pipeline_cls=NflH2hSnapshotPipeline,
        hit_rate_repo_cls=NflH2hHitRateReadRepository,
        snapshot_repo_cls=NflH2hSnapshotRepository,
    ),
    "nfl-spreads": SnapshotSpec(
        sport_key="americanfootball_nfl",
        market_key="spreads",
        pipeline_cls=NflSpreadsSnapshotPipeline,
        hit_rate_repo_cls=NflSpreadsHitRateReadRepository,
        snapshot_repo_cls=NflSpreadsSnapshotRepository,
    ),
    "nfl-totals": SnapshotSpec(
        sport_key="americanfootball_nfl",
        market_key="totals",
        pipeline_cls=NflTotalsSnapshotPipeline,
        hit_rate_repo_cls=NflTotalsHitRateReadRepository,
        snapshot_repo_cls=NflTotalsSnapshotRepository,
    ),
    "cfb-h2h": SnapshotSpec(
        sport_key="americanfootball_ncaaf",
        market_key="h2h",
        pipeline_cls=CfbH2hSnapshotPipeline,
        hit_rate_repo_cls=CfbH2hHitRateReadRepository,
        snapshot_repo_cls=CfbH2hSnapshotRepository,
    ),
    "cfb-spreads": SnapshotSpec(
        sport_key="americanfootball_ncaaf",
        market_key="spreads",
        pipeline_cls=CfbSpreadsSnapshotPipeline,
        hit_rate_repo_cls=CfbSpreadsHitRateReadRepository,
        snapshot_repo_cls=CfbSpreadsSnapshotRepository,
    ),
    "cfb-totals": SnapshotSpec(
        sport_key="americanfootball_ncaaf",
        market_key="totals",
        pipeline_cls=CfbTotalsSnapshotPipeline,
        hit_rate_repo_cls=CfbTotalsHitRateReadRepository,
        snapshot_repo_cls=CfbTotalsSnapshotRepository,
    ),
}

GRADE_SPECS: dict[str, GradeSpec] = {
    "nba-h2h": GradeSpec(
        sport_key="basketball_nba",
        market_key="h2h",
        pipeline_cls=NbaH2hGradePipeline,
        snapshot_read_repo_cls=NbaH2hSnapshotReadRepository,
        grade_repo_cls=NbaH2hGradeRepository,
    ),
    "nba-spreads": GradeSpec(
        sport_key="basketball_nba",
        market_key="spreads",
        pipeline_cls=NbaSpreadsGradePipeline,
        snapshot_read_repo_cls=NbaSpreadsSnapshotReadRepository,
        grade_repo_cls=NbaSpreadsGradeRepository,
    ),
    "nba-totals": GradeSpec(
        sport_key="basketball_nba",
        market_key="totals",
        pipeline_cls=NbaTotalsGradePipeline,
        snapshot_read_repo_cls=NbaTotalsSnapshotReadRepository,
        grade_repo_cls=NbaTotalsGradeRepository,
    ),
    "mlb-h2h": GradeSpec(
        sport_key="baseball_mlb",
        market_key="h2h",
        pipeline_cls=MlbH2hGradePipeline,
        snapshot_read_repo_cls=MlbH2hSnapshotReadRepository,
        grade_repo_cls=MlbH2hGradeRepository,
    ),
    "mlb-spreads": GradeSpec(
        sport_key="baseball_mlb",
        market_key="spreads",
        pipeline_cls=MlbSpreadsGradePipeline,
        snapshot_read_repo_cls=MlbSpreadsSnapshotReadRepository,
        grade_repo_cls=MlbSpreadsGradeRepository,
    ),
    "mlb-totals": GradeSpec(
        sport_key="baseball_mlb",
        market_key="totals",
        pipeline_cls=MlbTotalsGradePipeline,
        snapshot_read_repo_cls=MlbTotalsSnapshotReadRepository,
        grade_repo_cls=MlbTotalsGradeRepository,
    ),
    "nfl-h2h": GradeSpec(
        sport_key="americanfootball_nfl",
        market_key="h2h",
        pipeline_cls=NflH2hGradePipeline,
        snapshot_read_repo_cls=NflH2hSnapshotReadRepository,
        grade_repo_cls=NflH2hGradeRepository,
    ),
    "nfl-spreads": GradeSpec(
        sport_key="americanfootball_nfl",
        market_key="spreads",
        pipeline_cls=NflSpreadsGradePipeline,
        snapshot_read_repo_cls=NflSpreadsSnapshotReadRepository,
        grade_repo_cls=NflSpreadsGradeRepository,
    ),
    "nfl-totals": GradeSpec(
        sport_key="americanfootball_nfl",
        market_key="totals",
        pipeline_cls=NflTotalsGradePipeline,
        snapshot_read_repo_cls=NflTotalsSnapshotReadRepository,
        grade_repo_cls=NflTotalsGradeRepository,
    ),
    "cfb-h2h": GradeSpec(
        sport_key="americanfootball_ncaaf",
        market_key="h2h",
        pipeline_cls=CfbH2hGradePipeline,
        snapshot_read_repo_cls=CfbH2hSnapshotReadRepository,
        grade_repo_cls=CfbH2hGradeRepository,
    ),
    "cfb-spreads": GradeSpec(
        sport_key="americanfootball_ncaaf",
        market_key="spreads",
        pipeline_cls=CfbSpreadsGradePipeline,
        snapshot_read_repo_cls=CfbSpreadsSnapshotReadRepository,
        grade_repo_cls=CfbSpreadsGradeRepository,
    ),
    "cfb-totals": GradeSpec(
        sport_key="americanfootball_ncaaf",
        market_key="totals",
        pipeline_cls=CfbTotalsGradePipeline,
        snapshot_read_repo_cls=CfbTotalsSnapshotReadRepository,
        grade_repo_cls=CfbTotalsGradeRepository,
    ),
}


def parse_observation_time(value: str) -> datetime:
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed


def default_observation_time() -> datetime:
    return datetime.now(timezone.utc)


def resolve_observation_time(value: datetime | None) -> datetime:
    if value is not None:
        return value
    return default_observation_time()


def create_snapshot_pipeline(subcommand: str, db) -> Any:
    spec = SNAPSHOT_SPECS.get(subcommand)
    if spec is None:
        raise ValueError(f"Unknown snapshot subcommand: {subcommand!r}")
    return spec.pipeline_cls(
        odds_repo=FeaturedOddsReadRepository(db),
        hit_rate_repo=spec.hit_rate_repo_cls(db),
        snapshot_repo=spec.snapshot_repo_cls(db),
    )


def create_grade_pipeline(subcommand: str, db) -> Any:
    spec = GRADE_SPECS.get(subcommand)
    if spec is None:
        raise ValueError(f"Unknown grade subcommand: {subcommand!r}")
    return spec.pipeline_cls(
        snapshot_read_repo=spec.snapshot_read_repo_cls(db),
        games_repo=GamesReadRepository(db),
        grade_repo=spec.grade_repo_cls(db),
    )


def run_snapshot(subcommand: str, observation_time: datetime) -> SnapshotRunResult:
    spec = SNAPSHOT_SPECS.get(subcommand)
    if spec is None:
        raise ValueError(f"Unknown snapshot subcommand: {subcommand!r}")

    with get_db() as db:
        ensure_owned_tables(db)
        pipeline = create_snapshot_pipeline(subcommand, db)
        request = SnapshotRequest(
            sport_key=spec.sport_key,
            market_key=spec.market_key,
            observation_time=observation_time,
        )
        return pipeline.run(request)


def run_grade(subcommand: str, event_id: str | None = None) -> GradeRunResult:
    spec = GRADE_SPECS.get(subcommand)
    if spec is None:
        raise ValueError(f"Unknown grade subcommand: {subcommand!r}")

    with get_db() as db:
        ensure_owned_tables(db)
        pipeline = create_grade_pipeline(subcommand, db)
        request = GradeRequest(
            sport_key=spec.sport_key,
            market_key=spec.market_key,
            event_id=event_id,
        )
        return pipeline.run(request)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="BettorIndex data pipelines — snapshot, grade, and export pregame datasets.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot_parser = subparsers.add_parser(
        "snapshot",
        help="Build append-only pregame feature snapshots from upstream odds and hit rates.",
    )
    snapshot_subparsers = snapshot_parser.add_subparsers(
        dest="snapshot_type",
        required=True,
    )

    for name in sorted(SNAPSHOT_SPECS):
        cmd_parser = snapshot_subparsers.add_parser(
            name,
            help=f"Snapshot {SNAPSHOT_SPECS[name].sport_key} {SNAPSHOT_SPECS[name].market_key} markets.",
        )
        cmd_parser.add_argument(
            "--observation-time",
            default=None,
            type=parse_observation_time,
            help="ISO-8601 cutoff for pregame joins (defaults to current UTC time).",
        )

    grade_parser = subparsers.add_parser(
        "grade",
        help="Write post-game win/loss/push labels for completed snapshot rows.",
    )
    grade_subparsers = grade_parser.add_subparsers(
        dest="grade_type",
        required=True,
    )

    for name in sorted(GRADE_SPECS):
        cmd_parser = grade_subparsers.add_parser(
            name,
            help=f"Grade {GRADE_SPECS[name].sport_key} {GRADE_SPECS[name].market_key} snapshots.",
        )
        cmd_parser.add_argument(
            "--event-id",
            default=None,
            help="Optional Odds API event id filter (grades all eligible snapshots when omitted).",
        )

    return parser


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
    )
    args = build_parser().parse_args(argv)

    if args.command == "snapshot":
        result = run_snapshot(
            args.snapshot_type,
            resolve_observation_time(args.observation_time),
        )
        print(
            "Snapshot complete "
            f"candidates={result.candidates} "
            f"snapshotted={result.snapshotted} "
            f"skipped_existing={result.skipped_existing} "
            f"skipped_leakage={result.skipped_leakage}",
        )
        return 0

    if args.command == "grade":
        result = run_grade(args.grade_type, args.event_id)
        print(
            "Grade complete "
            f"candidates={result.candidates} "
            f"graded={result.graded} "
            f"skipped_existing={result.skipped_existing} "
            f"skipped_ungradeable={result.skipped_ungradeable}",
        )
        return 0

    logger.error("Unsupported command: %s", args.command)
    return 1


if __name__ == "__main__":
    sys.exit(main())
