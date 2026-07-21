"""Routes MLB prop markets to market-specific snapshot builders and repositories."""

from dataclasses import dataclass
from typing import TYPE_CHECKING

from schemas.mlb_batter_hits_snapshot import BATTER_HITS_MARKET_KEY, BATTER_HITS_SNAPSHOT_VERSION

if TYPE_CHECKING:
    from interfaces.market_snapshot_builder_interface import MarketSnapshotBuilderInterface
    from interfaces.mlb_batter_hits_snapshot_repository_interface import (
        MLBBatterHitsSnapshotRepositoryInterface,
    )


class UnsupportedMLBMarketError(ValueError):
    """Raised when an MLB market is unknown or not yet supported for snapshots."""


@dataclass(frozen=True)
class MLBMarketSnapshotEntry:
    """Registry metadata and wiring for one MLB prop market."""

    market_key: str
    supported: bool
    snapshot_version: str
    builder: "MarketSnapshotBuilderInterface | None" = None
    snapshot_repository: "MLBBatterHitsSnapshotRepositoryInterface | None" = None


MLB_MARKET_REGISTRY: dict[str, MLBMarketSnapshotEntry] = {
    BATTER_HITS_MARKET_KEY: MLBMarketSnapshotEntry(
        market_key=BATTER_HITS_MARKET_KEY,
        supported=True,
        snapshot_version=BATTER_HITS_SNAPSHOT_VERSION,
    ),
    "batter_total_bases": MLBMarketSnapshotEntry(
        market_key="batter_total_bases",
        supported=False,
        snapshot_version="batter_total_bases_v1",
    ),
}


def resolve_mlb_market(market_key: str) -> MLBMarketSnapshotEntry:
    """Return registry entry for a supported MLB market or raise a clear error."""
    normalized = market_key.strip().lower()
    entry = MLB_MARKET_REGISTRY.get(normalized)
    if entry is None:
        raise UnsupportedMLBMarketError(
            f"Unknown MLB snapshot market {market_key!r}. "
            f"Known markets: {sorted(MLB_MARKET_REGISTRY)}"
        )
    if not entry.supported:
        raise UnsupportedMLBMarketError(
            f"MLB snapshot market {market_key!r} is not supported yet "
            f"(planned snapshot_version={entry.snapshot_version!r})."
        )
    return entry


def register_mlb_market(entry: MLBMarketSnapshotEntry) -> None:
    """Attach builder/repo wiring for a supported market (used at CLI startup)."""
    existing = MLB_MARKET_REGISTRY.get(entry.market_key)
    if existing is None:
        raise UnsupportedMLBMarketError(
            f"Cannot register unknown MLB snapshot market {entry.market_key!r}"
        )
    if not existing.supported:
        raise UnsupportedMLBMarketError(
            f"Cannot register unsupported MLB snapshot market {entry.market_key!r}"
        )
    MLB_MARKET_REGISTRY[entry.market_key] = entry
