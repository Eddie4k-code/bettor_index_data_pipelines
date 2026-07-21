"""Market-specific pregame snapshot record for MLB ``batter_hits``."""

from datetime import datetime

from pydantic import Field, model_validator

from schemas.snapshot import PregameSnapshotRecordBase

BATTER_HITS_SNAPSHOT_VERSION = "batter_hits_v1"
BATTER_HITS_MARKET_KEY = "batter_hits"


class MLBBatterHitsSnapshotRecord(PregameSnapshotRecordBase):
    """Pregame snapshot row for ``mlb_batter_hits_pregame_snapshots``."""

    market_key: str = Field(default=BATTER_HITS_MARKET_KEY)
    snapshot_version: str = Field(default=BATTER_HITS_SNAPSHOT_VERSION)
    ten_game_hit_rate: float | None = None
    thirty_game_hit_rate: float | None = None
    sixty_game_hit_rate: float | None = None
    hit_rate_market_last_update: datetime

    @model_validator(mode="after")
    def _validate_market_key(self) -> "MLBBatterHitsSnapshotRecord":
        if self.market_key != BATTER_HITS_MARKET_KEY:
            raise ValueError(f"market_key must be {BATTER_HITS_MARKET_KEY!r}")
        return self
