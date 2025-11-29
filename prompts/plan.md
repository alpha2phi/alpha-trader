Goal: Build and deliver the Market Sentiment Dashboard per requirements.md and specs/001-market-sentiment-dashboard/spec.md.

Tech stack: Next.js (React + TS) frontend with SWR/React Query and a chart lib (Recharts or TradingView lightweight); FastAPI backend with Pydantic schemas; Redis for cache/TTL; Postgres for provenance; Celery/APScheduler for scheduled pulls.

Scope:
- Sentiment snapshot: Fear & Greed + VIX cards with freshness/stale badges, per-card retries, cache fallback.
- Cross-market candles: S&P 500, Nasdaq, Dow, BTC, ETH, SOL with 1D/1W/1M toggles, per-symbol freshness, cached fallback.
- Boosters: 10Y yield, breadth, macro events (2-week window); retries and stale handling.
- Shared market_data_service with single caching layer; provenance stored under data/provenance/market-sentiment/.
- Observability: metrics for latency/cache hits/error counts/stale serves; golden fixtures in tests/fixtures/golden/market_sentiment/.

Ask: Produce a milestone-based delivery plan with swimlanes (API clients, caching/jobs, UI/cards/charts, observability/tests). Sequence scheduled jobs per cadence (15m candles, 2h sentiment, 24h boosters), retries/backoff, and CI tests (contract/unit/integration). Keep it concise and actionable.
