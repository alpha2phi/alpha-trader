# Data Model: Market Sentiment Dashboard

## Entities

- **MarketSentimentSnapshot**
  - Fields: `fear_greed_score` (int), `fear_greed_category` (string), `vix_level` (number), `vix_abs_change` (number), `vix_pct_change` (number), `updated_at` (datetime, UTC), `source` (string), `cache_state` (enum: fresh/stale)
  - Notes: Combines sentiment + volatility for single response; track provider used.

- **CandleSeries**
  - Fields: `symbol` (string), `timeframe` (enum: 1D/1W/1M), `ohlcv` (array of {open, high, low, close, volume, ts}), `timezone` (string), `last_updated` (datetime, UTC), `cache_state` (enum: fresh/stale)
  - Notes: Supports index (^GSPC, ^IXIC, ^DJI) and crypto (BTC-USD, ETH-USD, SOL-USD).

- **BoosterSignal**
  - Fields: `name` (string), `value` (number/string), `unit` (string), `change` (number, optional), `threshold_highlight` (string/enum), `updated_at` (datetime, UTC), `source` (string), `cache_state` (enum: fresh/stale)
  - Notes: Used for 10Y yield, breadth; threshold_highlight flags notable levels.

- **MacroEvent**
  - Fields: `title` (string), `datetime_utc` (datetime), `impact` (string/enum), `source` (string), `updated_at` (datetime, UTC)
  - Notes: Included as array within boosters payload; 2-week window.

- **ProvenanceRecord**
  - Fields: `source` (string), `payload_checksum` (string), `fetched_at` (datetime, UTC), `cache_key` (string), `storage_ref` (string to file or DB record)
  - Notes: Supports auditability for all upstream fetches.

## Relationships

- `MarketSentimentSnapshot` references provenance via `source`/`cache_key`.
- `CandleSeries` linked to provenance per `symbol` + `timeframe`.
- `BoosterSignal` and `MacroEvent` share booster provenance entries.

## Validation Rules

- All timestamps must be UTC and present.
- `cache_state` determined by TTL per signal (sentiment 2h, candles 15m, boosters 24h).
- Symbols constrained to allowed set unless extended via config.
