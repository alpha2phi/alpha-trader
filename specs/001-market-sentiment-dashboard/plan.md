# Implementation Plan: Market Sentiment Dashboard

**Branch**: `[001-market-sentiment-dashboard]` | **Date**: 2025-11-29 | **Spec**: specs/001-market-sentiment-dashboard/spec.md
**Input**: Feature specification from `/specs/001-market-sentiment-dashboard/spec.md`

## Summary

Deliver a web dashboard that surfaces Fear & Greed + VIX sentiment, multi-asset candlestick charts (S&P 500, Nasdaq, Dow, BTC, ETH, SOL), and booster signals (10Y yield, breadth, macro events) with freshness/stale indicators, per-card retries, and cached fallbacks. Stack: Next.js (React + TS) frontend with React Query and Recharts; FastAPI backend with Pydantic schemas; Redis TTL cache; Postgres provenance storage; Celery workers with APScheduler triggers for cadenced fetches (15m candles, 2h sentiment, 24h boosters). Observability covers latency/cache hits/error counts/stale serves with golden fixtures for replay tests.

## Technical Context
**Language/Version**: Python 3.11 (backend), TypeScript/Next.js 14 (frontend)  
**Primary Dependencies**: FastAPI, Pydantic, Redis client, Celery, APScheduler; Next.js, React Query/SWR, Recharts (TradingView lightweight fallback), Axios/fetch  
**Storage**: Redis for cache, Postgres for provenance/file drops under `data/provenance/market-sentiment/`  
**Testing**: pytest, requests-mock, Jest/React Testing Library, Playwright smoke, contract tests via OpenAPI schemas  
**Target Platform**: Web app (Next.js) + Linux-hosted API services  
**Project Type**: Web (frontend + backend)  
**Performance Goals**: UI shows sentiment data within 3s; chart toggles update under 2s; booster freshness ≤24h; 95% of loads served from valid cache; 60fps chart interaction goal  
**Constraints**: TTLs (sentiment 2h, candles 15m, boosters 24h); honor provider rate limits/429 backoff; UTC normalization; additive contracts (Never Break Userspace)  
**Scale/Scope**: Single dashboard surface covering 6 symbols + 3 boosters; moderate concurrent users; extensible to new symbols/providers via shared market_data_service

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*
- **General Solution Proof**: Use a shared `market_data_service` abstraction for all providers (sentiment, volatility, index/crypto OHLC, boosters) with provider priority tables and uniform cache/provenance handling to avoid per-widget branching.
- **Compatibility Contract**: Preserve existing exports/field names where present; additive contracts for new fields; contract tests enforce schemas for `/sentiment`, `/candles`, `/boosters`; migrations not required beyond new endpoints.
- **Pragmatic Scenario & Value**: Primary workflow: trader checks Fear & Greed + VIX, validates with cross-market candles, and inspects boosters before acting; MVP slices ship independently per story (sentiment first, charts second, boosters third).
- **Simplicity & Complexity Risks**: Risks: per-symbol/timeframe branching, retry logic duplication. Mitigation: single cache layer with TTL metadata, shared retry/backoff helper, normalized UTC timestamps/units.
- **Domain Guardrails**: Providers with cadences: sentiment hourly/2h TTL; VIX/indices 5–15m; crypto 1m; boosters daily. Secrets via env vars. Provenance persisted in Postgres plus files under `data/provenance/market-sentiment/`. Licensing and rate-limit adherence required.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
backend/
├── src/
│   ├── models/          # Pydantic schemas for sentiment, candles, boosters
│   ├── services/        # market_data_service, provider clients, caching
│   ├── api/             # FastAPI routers: sentiment, candles, boosters
│   └── jobs/            # Celery tasks, APScheduler triggers
└── tests/
    ├── contract/
    ├── integration/
    └── unit/

frontend/
├── src/
│   ├── components/      # Cards, charts, booster panels, shared UI
│   ├── pages/           # Next.js pages/routes
│   ├── services/        # API clients with React Query/SWR
│   └── lib/             # Types, formatters, caching helpers
└── tests/               # Jest/RTL, Playwright smoke

tests/fixtures/golden/market_sentiment/  # Shared golden payloads
data/provenance/market-sentiment/        # Raw provider drops
```

**Structure Decision**: Web application split into `backend/` (FastAPI, Celery/APScheduler) and `frontend/` (Next.js/TS), with shared test fixtures and provenance storage per spec.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
