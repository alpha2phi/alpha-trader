# Tasks: Market Sentiment Dashboard

**Input**: Design documents from `/specs/001-market-sentiment-dashboard/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup

- [ ] T001 Ensure backend/ and frontend/ project scaffolds align with plan in backend/ and frontend/
- [ ] T002 Add environment template with Redis/Postgres/provider keys in backend/.env.example
- [ ] T003 [P] Add environment template with API base URL in frontend/.env.example.local

## Phase 2: Foundational

- [ ] T004 Configure base FastAPI app wiring and health route in backend/src/api/__init__.py
- [ ] T005 Establish Redis/Postgres connection helpers and settings in backend/src/services/config.py
- [ ] T006 [P] Implement cache wrapper with TTL/stale calculation in backend/src/services/cache.py
- [ ] T007 [P] Define shared provider priority config per signal in backend/src/services/provider_registry.py
- [ ] T008 Create core Pydantic models from data-model in backend/src/models/market.py
- [ ] T009 Add provenance writer (DB + file drop) in backend/src/services/provenance.py
- [ ] T010 [P] Set up React Query client/provider and API base client in frontend/src/services/api-client.ts
- [ ] T011 Add shared UI states (loading/error/stale badge components) in frontend/src/components/shared/status.tsx

## Phase 3: User Story 1 - Sentiment Snapshot (Priority: P1) 🎯 MVP

**Goal**: Deliver Fear & Greed + VIX cards with freshness/stale and retry.
**Independent Test**: Stub sentiment/VIX responses; cards render scores, categories, timestamps within 2s; retry uses cached fallback on failure.

### Tests for User Story 1

- [ ] T012 [P] [US1] Write contract test for GET /api/sentiment in backend/tests/contract/test_sentiment.py
- [ ] T013 [P] [US1] Write integration test simulating provider outage + cache fallback in backend/tests/integration/test_sentiment_fallback.py

### Implementation for User Story 1

- [ ] T014 [P] [US1] Implement sentiment provider client(s) with fallback order in backend/src/services/providers/sentiment.py
- [ ] T015 [P] [US1] Implement volatility (VIX) client with fallback order in backend/src/services/providers/volatility.py
- [ ] T016 [US1] Implement sentiment service (cache + provenance) in backend/src/services/sentiment_service.py
- [ ] T017 [US1] Expose /api/sentiment FastAPI router returning snapshot schema in backend/src/api/sentiment.py
- [ ] T018 [US1] Build sentiment cards with freshness/stale badges and retry in frontend/src/components/sentiment/SentimentCards.tsx
- [ ] T019 [P] [US1] Wire frontend data hook for sentiment (React Query) in frontend/src/services/hooks/useSentiment.ts
- [ ] T020 [US1] Add page section integration for sentiment cards in frontend/src/pages/index.tsx

## Phase 4: User Story 2 - Cross-Market Candles (Priority: P2)

**Goal**: Provide candlestick charts for S&P 500, Nasdaq, Dow, BTC, ETH, SOL with 1D/1W/1M toggles and freshness.
**Independent Test**: Cached OHLC data renders per symbol; toggles swap timeframes without full page refresh; stale indicator shown when data exceeds TTL.

### Tests for User Story 2

- [ ] T021 [P] [US2] Write contract test for GET /api/candles in backend/tests/contract/test_candles.py
- [ ] T022 [P] [US2] Integration test for timeframe toggle + stale fallback in backend/tests/integration/test_candles_timeframes.py

### Implementation for User Story 2

- [ ] T023 [P] [US2] Implement index OHLC client(s) with fallback order in backend/src/services/providers/index_ohlc.py
- [ ] T024 [P] [US2] Implement crypto OHLC client(s) with fallback order in backend/src/services/providers/crypto_ohlc.py
- [ ] T025 [US2] Implement candles service (per-symbol/timeframe cache, provenance) in backend/src/services/candles_service.py
- [ ] T026 [US2] Expose /api/candles FastAPI router with timeframe params in backend/src/api/candles.py
- [ ] T027 [US2] Build charts with 1D/1W/1M toggles and freshness text in frontend/src/components/charts/CandlesPanel.tsx
- [ ] T028 [P] [US2] Wire frontend data hook for candles (by symbol/timeframe) in frontend/src/services/hooks/useCandles.ts
- [ ] T029 [US2] Integrate charts into dashboard layout with per-symbol selection in frontend/src/pages/index.tsx

## Phase 5: User Story 3 - Simple Signal Boosters (Priority: P3)

**Goal**: Show 10Y yield, breadth, and 2-week macro events with freshness, thresholds, and retries.
**Independent Test**: Booster cards show values/timestamps; macro list loads events; retry restores data after simulated failure; stale indicators respect TTL.

### Tests for User Story 3

- [ ] T030 [P] [US3] Write contract test for GET /api/boosters in backend/tests/contract/test_boosters.py
- [ ] T031 [P] [US3] Integration test for booster retries + stale states in backend/tests/integration/test_boosters_retry.py

### Implementation for User Story 3

- [ ] T032 [P] [US3] Implement booster clients (10Y yield, breadth, macro events) with fallback order in backend/src/services/providers/boosters.py
- [ ] T033 [US3] Implement boosters service (cache/provenance/thresholds) in backend/src/services/boosters_service.py
- [ ] T034 [US3] Expose /api/boosters FastAPI router in backend/src/api/boosters.py
- [ ] T035 [US3] Build boosters panel (yield + delta, breadth highlight, macro events list) with retry/stale badges in frontend/src/components/boosters/BoostersPanel.tsx
- [ ] T036 [P] [US3] Wire frontend data hook for boosters in frontend/src/services/hooks/useBoosters.ts
- [ ] T037 [US3] Integrate boosters panel into dashboard layout in frontend/src/pages/index.tsx

## Phase 6: Schedulers & Observability

- [ ] T038 Configure APScheduler triggers for sentiment (2h), candles (15m), boosters (24h) invoking Celery tasks in backend/src/jobs/schedules.py
- [ ] T039 [P] Implement Celery tasks writing cache + provenance for all signals in backend/src/jobs/tasks.py
- [ ] T040 Add metrics/logging for latency, cache hit/miss, errors, stale serves in backend/src/services/observability.py
- [ ] T041 [P] Add golden fixtures for sentiment, candles, boosters in tests/fixtures/golden/market_sentiment/
- [ ] T042 Add Playwright/Jest smoke for dashboard loading and retries in frontend/tests/smoke/dashboard.spec.ts

## Phase 7: Polish & Cross-Cutting Concerns

- [ ] T043 Cleanup docs with quickstart references and provider notes in specs/001-market-sentiment-dashboard/quickstart.md
- [ ] T044 [P] Add README excerpt summarizing new endpoints and env vars in README.md
- [ ] T045 Performance pass: verify UI loads <3s and toggles <2s under stubbed data; document in specs/001-market-sentiment-dashboard/plan.md
- [ ] T046 [P] Security/compatibility sweep ensuring additive contracts and stable field names in backend/tests/contract/

## Dependencies & Execution Order

- Phase dependencies: Setup → Foundational → US1 (MVP) → US2 → US3 → Schedulers/Observability → Polish.
- User story completion order: US1 first (MVP), then US2, then US3; US2/US3 can run in parallel after Foundational if team capacity allows.

## Parallel Execution Examples

- Within US1: T014/T015 (provider clients) and T019 (data hook) can run in parallel; T016/T017 depend on clients; T018/T020 depend on API + hook.
- Within US2: T023/T024/T028 can run in parallel; T025 depends on clients; T026 after service; T027/T029 depend on API + hook.
- Within US3: T032/T036 parallel; T033 after clients; T034 after service; T035/T037 after API + hook.
- Cross-phase: T006/T007 cache/config can run alongside T010/T011 frontend setup once T004–T005 begin.

## Implementation Strategy

- MVP = Complete Phases 1–3 to ship sentiment snapshot independently, then iterate with US2, US3.
- Tests prioritized per contract/integration to uphold compatibility and fallback behavior; performance checks in Polish.
