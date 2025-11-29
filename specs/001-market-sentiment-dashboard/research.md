# Research: Market Sentiment Dashboard

## Decisions

- **Decision**: Use provider priority/fallback per signal (sentiment, VIX/index, crypto, boosters) with documented order.  
  **Rationale**: Reduces downtime and rate-limit risk while preserving consistent contracts.  
  **Alternatives considered**: Single provider per signal (too fragile); one vendor for all data (license/latency risk).

- **Decision**: Charts via Recharts (with TradingView lightweight as backup if candlestick fidelity is insufficient).  
  **Rationale**: Recharts integrates cleanly with React/TS and supports responsive rendering; fallback retains candlestick depth if needed.  
  **Alternatives considered**: D3 (more boilerplate), Chart.js (less candlestick support).

- **Decision**: Scheduler strategy is APScheduler to trigger Celery tasks for fetches (15m candles, 2h sentiment, 24h boosters) writing to Redis + provenance.  
  **Rationale**: Separates orchestration from workers; aligns with TTLs; supports backoff/retry policies.  
  **Alternatives considered**: Celery beat only (less flexible per-signal cadence); cronjobs (harder to observe and adjust).

- **Decision**: Provenance stored in Postgres plus file drops under `data/provenance/market-sentiment/` with timestamps.  
  **Rationale**: Durable audit trail and debuggable artifacts.  
  **Alternatives considered**: File-only (harder to query), DB-only (harder to inspect raw payloads).

## Resolved Unknowns

- Provider fallback ordering: defined per signal (above).
- Charting library: Recharts primary; TradingView lightweight fallback if needed.
- Scheduling cadence: APScheduler triggers Celery tasks at 15m/2h/24h aligned to TTLs.

## Open Items

- None flagged; spec clarifications currently satisfied.
