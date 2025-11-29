# Feature Specification: Market Sentiment Dashboard

**Feature Branch**: `[001-market-sentiment-dashboard]`  
**Created**: 2025-11-29  
**Status**: Draft  
**Input**: User description: "Start with fear and greed index, VIX, major index candlestick charts, and any other recommendable simple signals."

## Clarifications

### Session 2025-11-29

- Q: How should providers be selected and failed over per signal? -> A: Set a priority order per signal with explicit fallback rules.

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

> **Scenario-First Reminder**: Each story describes one trading workflow end-to-end (e.g.,
> "swing trader evaluates earnings momentum") and must remain shippable without other stories.

### User Story 1 - Sentiment Snapshot (Priority: P1)

An active trader opens the dashboard to instantly read current market mood via the Fear & Greed index and VIX so they can decide whether to trade aggressively or defensively.

**Why this priority**: Provides immediate directional context; without it the dashboard fails its primary purpose.

**Independent Test**: Stub sentiment responses (Fear & Greed score + category, VIX level + change) and confirm the dashboard renders both cards with freshness badges and color-coded categories within 2 seconds of load.

**Acceptance Scenarios**:

1. **Given** the user loads the dashboard with live data available, **When** values are retrieved, **Then** Fear & Greed and VIX cards show score/level, categorized sentiment (e.g., Extreme Fear), and last-updated time.
2. **Given** a sentiment provider is unreachable, **When** the dashboard loads, **Then** the affected card shows the last cached value, a stale indicator, and a visible retry control without blocking other cards.

---

### User Story 2 - Cross-Market Candles (Priority: P2)

A swing trader compares candlestick charts for S&P 500, Nasdaq, Dow, Bitcoin, Ethereum, and Solana to see if price action agrees with the sentiment read.

**Why this priority**: Visual confirmation of price trends is necessary to act on sentiment; charts make the dashboard usable beyond a headline score.

**Independent Test**: Provide cached OHLC data for all six symbols and verify each chart renders with selectable 1D/1W/1M ranges and reloads independently of sentiment cards.

**Acceptance Scenarios**:

1. **Given** OHLC data exists for each symbol, **When** the user switches between 1D/1W/1M, **Then** the selected chart updates without full page refresh and shows the new time range label.
2. **Given** a symbol lacks fresh candles, **When** the user views that chart, **Then** the dashboard falls back to the latest cached series, surfaces last-update time, and continues to load other symbols normally.

---

### User Story 3 - Simple Signal Boosters (Priority: P3)

A portfolio manager checks quick secondary signals—10Y Treasury yield, market breadth for S&P 500, and a two-week macro event list—to understand catalysts behind sentiment shifts.

**Why this priority**: Boosters enrich interpretation and are valuable but can ship after the core sentiment + charts MVP.

**Independent Test**: Mock each booster data feed and confirm each card updates independently, with its own loading/error states, without blocking sentiment or chart rendering.

**Acceptance Scenarios**:

1. **Given** booster data is available, **When** the user opens the boosters panel, **Then** the dashboard shows yield level + day-over-day change, breadth percentage with threshold highlight, and upcoming events with timestamps.
2. **Given** the macro events feed fails, **When** the user expands events, **Then** the panel shows a retry control, last-known schedule, and continues showing other boosters.

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

- Provider rate limits or HTTP 429 responses while other sources remain healthy.
- Partial sentiment availability (e.g., VIX present but Fear & Greed missing).
- Symbol changes or delistings for tracked indexes/coins.
- User attempts rapid refreshes across multiple widgets simultaneously.
- Data older than stated TTLs when markets are closed or during outages.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST surface the current Fear & Greed score with category label and last-updated time.
- **FR-002**: System MUST display the current VIX level with absolute and percentage day-over-day change plus freshness timestamp.
- **FR-003**: Users MUST be able to view candlestick charts for S&P 500, Nasdaq, Dow, Bitcoin, Ethereum, and Solana with selectable 1D, 1W, and 1M ranges.
- **FR-004**: System MUST show per-symbol last updated time and explicitly indicate when chart data is stale.
- **FR-005**: System MUST provide per-card retry controls that reattempt data fetch without reloading the full dashboard.
- **FR-006**: System MUST present simple booster signals: 10Y Treasury yield with daily delta, S&P 500 breadth (% constituents above 50DMA), and a two-week macro events list with timestamps.
- **FR-007**: System MUST cache provider responses with defined TTLs and mark data as stale once TTL is exceeded.
- **FR-008**: System MUST continue rendering healthy widgets when one or more data sources fail, showing error messaging confined to the affected card.
- **FR-009**: System MUST align values to a consistent timezone (UTC) and units (e.g., yield in %, breadth in %) across all widgets.

### Key Entities *(include if feature involves data)*

- **MarketSentimentSnapshot**: Fear & Greed score, categorical label, source, last-updated timestamp.
- **VolatilityReading**: VIX level, absolute/percent change, source, timestamp, cache state.
- **CandleSeries**: Symbol, timeframe, array of OHLCV candles, timezone, last-update metadata, cache status.
- **BoosterSignal**: Generic signal envelope (name, value, unit, change/thresholds, timestamp, source, cache status).
- **MacroEvent**: Event name, scheduled UTC datetime, expected impact, last-updated, data source.

## Compatibility & Simplicity Constraints *(mandatory)*

- **Existing Consumers**: Preserve any existing exports or CLI outputs for sentiment/market data by keeping field names stable where already used; add new fields without removing current ones.
- **Migration Plan**: Ship core sentiment + chart widgets first; release boosters behind a toggle so early users are unaffected by booster delays or missing licenses.
- **Simplification Work**: Centralize data retrieval through a shared market data access layer with a single caching policy to avoid per-widget fetch logic and duplicated error handling.

## Data Sources & Compliance *(mandatory for every feature touching market data)*

| Source | Purpose | Endpoint / Query Params | Refresh Cadence | Compliance / License Notes |
|--------|---------|-------------------------|-----------------|---------------------------|
| Sentiment feed (Fear & Greed) | Sentiment score + category | Sentiment summary endpoint or scrape | Hourly | Confirm terms of use; note attribution requirements |
| Volatility feed | VIX quote and change | Quote endpoint for volatility index | 5 min | Verify redistribution rights; respect rate limits |
| Index OHLC provider | Candles for S&P 500, Nasdaq, Dow | Aggregates endpoint per symbol/timeframe | 5–15 min | Ensure symbol mapping accuracy and licensing for index data |
| Crypto OHLC provider | Candles for BTC, ETH, SOL | Market data endpoint with timeframe param | 1 min | Confirm exchange redistribution allowances |
| Macro/indicator provider | 10Y yield, breadth, macro calendar | Indicator and calendar endpoints | Daily | Validate licensing for breadth inputs and event metadata |

- Secrets storing credentials: `SENTIMENT_API_KEY`, `MARKET_DATA_API_KEY`, `MACRO_DATA_API_KEY` (or equivalents defined in env).
- Cache retention policy: sentiment hourly, VIX and index/crypto candles 15 minutes, boosters daily; invalidate cache on manual refresh or TTL expiry.
- Provenance evidence to attach in release: store raw provider responses with timestamps under `data/provenance/market-sentiment/`.
- Provider strategy: document per-signal primary and fallback providers following the priority order approach above; fall back on failure while honoring rate limits and licensing.

## Analytics Contracts & Explainability *(required for each analytic module)*

- **Module Name**: `sentiment_snapshot`
  - CLI invocation: `python -m sentiment_snapshot`
  - Inputs: credentials for sentiment and volatility feeds, cache layer.
  - Outputs: `{ "fear_greed": { "score": int, "category": string, "updated_at": iso8601 }, "vix": { "level": number, "abs_change": number, "pct_change": number, "updated_at": iso8601 } }`.
  - Explainability notes: expose provider name, data timestamp, and category mapping logic for Fear & Greed.

- **Module Name**: `market_charts`
  - CLI invocation: `python -m market_charts --symbols ^GSPC,^IXIC,^DJI,BTC,ETH,SOL --range 1D`
  - Inputs: symbol list, timeframe selection, cache layer.
  - Outputs: per-symbol OHLCV arrays plus last-updated metadata and timezone info.
  - Explainability notes: document timeframe normalization, handling of missing candles, and currency units for crypto.

- **Module Name**: `signal_boosters`
  - CLI invocation: `python -m signal_boosters --signals ten_year_yield,breadth,macro_events`
  - Inputs: booster list, credentials for macro/indicator data, cache layer.
  - Outputs: structured signals with value, unit, change/threshold highlights, and events list with timestamps.
  - Explainability notes: include calculation notes for breadth (percentage above 50DMA) and highlight when data is stale.

## Observability & Risk Controls *(describe monitoring + tests)*

- Logs/metrics: per-source latency, cache hit rate, fetch success/fail counts, and stale-data served counts per widget.
- Golden datasets: canned sentiment, VIX, OHLC, and macro samples stored under `tests/fixtures/golden/market_sentiment/` for replay tests.
- Tests planned:
  - Contract: validate JSON schema for sentiment snapshot, chart payload, and booster signals.
  - Unit: cache TTL behavior, timeframe toggling logic, breadth calculation, and stale-flag handling.
  - Integration: simulate provider outages/rate limits to ensure unaffected widgets render and retries work without page reload.
- Alerting: trigger alerts when error rate for any provider exceeds 10% over 15 minutes or when stale data age exceeds 1.5x TTL.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of dashboard loads present current (≤2h old) Fear & Greed and VIX data within 3 seconds.
- **SC-002**: Users can switch between 1D/1W/1M views for any chart with updated data visible in under 2 seconds in 95% of attempts.
- **SC-003**: Booster signals remain ≤24h old on trading days, with fetch failure rate under 5% per source.
- **SC-004**: At least 80% of surveyed beta users report the dashboard helps them assess market conditions faster than their prior workflow.
