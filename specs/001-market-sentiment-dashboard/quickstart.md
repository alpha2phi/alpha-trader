# Quickstart: Market Sentiment Dashboard

## API Smoke

1. Start backend with FastAPI server.  
2. Call `GET /api/sentiment` -> expect Fear & Greed + VIX with `cache_state` and `updated_at`.  
3. Call `GET /api/candles?symbol=^GSPC&timeframe=1D` -> expect OHLCV array and `cache_state`.  
4. Call `GET /api/boosters` -> expect 10Y, breadth, macro events (2-week window) with timestamps.

## Frontend Smoke

1. Run Next.js dev server.  
2. Load dashboard: sentiment cards show freshness/stale badges and retry buttons.  
3. Toggle charts across 1D/1W/1M for S&P 500 and BTC; verify per-symbol freshness text.  
4. Expand boosters panel: see 10Y + delta, breadth highlight, upcoming macro events; trigger retry on boosters.

## Jobs & Cache

1. Trigger APScheduler/Celery tasks manually: sentiment (2h cadence), candles (15m per symbol), boosters (24h).  
2. Verify Redis entries include TTL metadata and `cache_state` flips to `stale` after expiry.  
3. Check provenance: Postgres records plus file drops under `data/provenance/market-sentiment/`.

## Tests

- Contract tests: validate `/api/sentiment`, `/api/candles`, `/api/boosters` schemas.  
- Unit tests: cache TTL logic, provider fallback, breadth calculation, chart timeframe switch.  
- Integration: simulate provider 429/outage; ensure cached fallback + stale indicators and unaffected widgets render.  
- Fixtures: replay golden payloads from `tests/fixtures/golden/market_sentiment/`.
