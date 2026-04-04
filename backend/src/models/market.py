from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field

CacheState = Literal["fresh", "stale"]
Timeframe = Literal["1D", "1W", "1M"]


class FearGreed(BaseModel):
    score: int
    category: str
    updated_at: datetime
    cache_state: CacheState
    provider: Optional[str] = None


class VixReading(BaseModel):
    level: float
    abs_change: float
    pct_change: float
    updated_at: datetime
    cache_state: CacheState
    provider: Optional[str] = None


class MarketSentimentSnapshot(BaseModel):
    fear_greed: FearGreed
    vix: VixReading


class Candle(BaseModel):
    ts: datetime = Field(..., description="Timestamp in UTC")
    open: float
    high: float
    low: float
    close: float
    volume: float


class CandleSeries(BaseModel):
    symbol: str
    timeframe: Timeframe
    timezone: str
    cache_state: CacheState
    last_updated: datetime
    ohlcv: List[Candle]


class BoosterSignal(BaseModel):
    name: str
    value: float
    unit: str
    change: Optional[float] = None
    threshold_highlight: Optional[str] = None
    updated_at: datetime
    cache_state: CacheState
    provider: Optional[str] = None


class MacroEvent(BaseModel):
    title: str
    datetime_utc: datetime
    impact: Optional[str] = None
    source: Optional[str] = None
    updated_at: datetime


class Boosters(BaseModel):
    ten_year_yield: BoosterSignal
    breadth: BoosterSignal
    macro_events: List[MacroEvent]
