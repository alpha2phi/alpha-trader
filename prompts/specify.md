# Feature Specification: Market Sentiment Starter Dashboard

**Feature Branch**: `[001-market-sentiment-dashboard]`  
**Created**: 2024-02-16  
**Status**: Draft  
**Input**: User description: "Start with fear and greed index, VIX, major index candlestick charts, and any other recommendable simple signals."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Risk Sentiment Snapshot (Priority: P1)

An active trader opens the dashboard to instantly read the CNN Fear & Greed index alongside live VIX values, so they gauge if markets are fearful or greedy before making trades.

**Why this priority**: Without a sentiment snapshot the dashboard lacks immediate value and cannot inform any workflow; it is the MVP slice.

**Independent Test**: Stub the sentiment API responses (fear & greed index + VIX) and verify the dashboard renders both metrics, freshness indicators, and alert colors inside 2 seconds.

**Acceptance Scenarios**:

1. **Given** the user loads the dashboard, **When** the APIs respond with latest values, **Then** fear/greed and VIX cards display with categorized sentiment (e.g., "Extreme Fear").
2. **Given** a provider times out, **When** the user loads the dashboard, **Then** the affected card shows the last cached value with a stale badge and error tooltip.

---

### User Story 2 - Index & Crypto Trend Visualization (Priority: P2)

A swing trader compares candlestick charts for S&P 500, Nasdaq, Dow, plus BTC, ETH, and SOL to spot cross-market flows and confirm whether overall trend matches the sentiment reading.

**Why this priority**: Index candles contextualize sentiment moves; traders often validate signals visually before acting.

**Independent Test**: Feed cached OHLC data for the three indexes and the three crypto assets and confirm each chart loads independently with timeframe toggles, even if sentiment services are offline.

**Acceptance Scenarios**:

1. **Given** OHLC data exists for each index and crypto asset, **When** the user toggles between 1D/1W/1M views, **Then** charts re-render without full page refresh.
2. **Given** an asset lacks fresh candles, **When** the user selects that symbol, **Then** the UI falls back to the most recent dataset and displays last update time.

---

### User Story 3 - Macro Context Boosters (Priority: P3)

A portfolio manager checks supporting indicators—10Y Treasury yield, market breadth (% S&P names above 50DMA), and a near-term macro calendar—to anticipate catalysts.

**Why this priority**: These metrics enrich the dashboard and help interpret sentiment volatility; they can release after the base view ships.

**Independent Test**: Simulate data fetches for each booster and validate each card updates separately with dedicated error states, independent of the sentiment and charts.

**Acceptance Scenarios**:

1. **Given** macro data is available, **When** the user opens the boosters panel, **Then** they see yield level, breadth percentage, and upcoming CPI/FOMC events with respective timestamps.
2. **Given** the macro calendar API fails, **When** the user attempts to expand events, **Then** the system surfaces a retry button plus a cached last-known schedule.

---

### Edge Cases

- What happens when any provider hits its rate limit or returns HTTP 429?
- How does the system react if only partial sentiment data is available (e.g., VIX but not fear/greed)?
- How are delisted or renamed indexes handled if provider symbols change?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST retrieve and display the CNN Fear & Greed index category and numerical score with freshness metadata.
- **FR-002**: System MUST retrieve the current VIX level with day-over-day delta and percent change.
- **FR-003**: Users MUST be able to view candlestick charts for S&P 500, Nasdaq, Dow, Bitcoin, Ethereum, and Solana with selectable timeframes (1D/1W/1M).
- **FR-004**: System MUST show the 10Y Treasury yield level and daily delta sourced from FRED or similar provider.
- **FR-005**: System MUST calculate or ingest a market breadth percentage (S&P 500 constituents above 50DMA) and highlight thresholds.
- **FR-006**: System MUST display an upcoming macro-event list (e.g., CPI, FOMC, jobs report) covering at least the next two weeks.
- **FR-007**: System MUST cache provider responses with TTLs and present stale data indicators when serving cached values.
- **FR-008**: System MUST log provider errors and expose a retry control per widget when data fetch fails (NEEDS CLARIFICATION: UI interaction for retries).

### Key Entities

- **MarketSentimentSnapshot**: Combines fear/greed score, VIX level, timestamp, provider metadata.
- **IndexCandleSeries**: Symbol identifier (e.g., `^GSPC`, `BTC-USD`), timeframe, array of OHLCV candles, last update timestamp.
- **MacroIndicator**: Generic structure for booster metrics (10Y yield, breadth) storing value, unit, trend, and caching data.
- **MacroEvent**: Upcoming event name, date/time (UTC), impact rating, data source.

## Compatibility & Simplicity Constraints *(mandatory)*

- **Existing Consumers**: Preserve any current CLI or script exports by keeping JSON field names stable (`fear_greed.score`, `vix.level`, `indexes[].symbol`, etc.).
- **Migration Plan**: Introduce new boosters behind a feature flag so the base sentiment + chart view ships first; ensure exports add fields without removing existing ones.
- **Simplification Work**: Centralize provider access through a shared `market_data_service` to avoid bespoke fetch logic per widget; enforce a single caching layer for all signals.

## Data Sources & Compliance *(mandatory for every feature touching market data)*

| Source | Purpose | Endpoint / Query Params | Refresh Cadence | Compliance / License Notes |
|--------|---------|-------------------------|-----------------|---------------------------|
| CNN Fear & Greed (unofficial JSON scrape) | Sentiment score | `https://money.cnn.com/` scrape or mirroring endpoint | Hourly | Confirm ToS; consider proxy API for reliability |
| CBOE / Polygon / Alpha Vantage | VIX quote | `/v2/aggs/ticker/VIX/...` | 5 min | Attribute CBOE data, honor rate limits |
| Polygon / Alpha Vantage | Index OHLC data | `/v2/aggs/ticker/{symbol}/range/{interval}` | 5 min (1D) | Document symbol mapping (`^GSPC`, `^IXIC`, `^DJI`) |
| Coinbase / Kraken / Polygon | Crypto OHLC data | `/v1/marketdata/{symbol}/candles?interval=...` | 1 min | Confirm exchange data redistribution rights; symbolize `BTC-USD`, `ETH-USD`, `SOL-USD` |
| FRED API | 10Y Treasury yield | `/fred/series/observations?series_id=DGS10` | Daily | API key stored in `FRED_API_KEY`; cite FRED |
| Internal calc (requires S&P constituents) | Breadth | Derived from component OHLC data | Daily | Requires licensed constituent data—confirm redistribution rights |
| Financial Modeling Prep / Econoday | Macro calendar | `/economic_calendar` | Daily | Ensure usage allowed; upcoming event metadata may require attribution |

- Secrets storing credentials: `POLYGON_API_KEY`, `ALPHAVANTAGE_KEY`, `FRED_API_KEY`, `FMP_API_KEY`.
- Cache retention policy: fear/greed 2h; VIX/index candles 15m; 10Y yield/breadth 24h; macro calendar refresh daily at 00:00 UTC or on demand.
- Provenance evidence: persist provider responses plus checksum under `data/provenance/market-sentiment/<source>/<timestamp>.json`.

## Analytics Contracts & Explainability *(required for each analytic module)*

- **Module Name**: `services/sentiment_snapshot.py`
  - CLI invocation: `python -m services.sentiment_snapshot --ticker-set default`
  - Inputs: provider credentials, cache layer.
  - Outputs: JSON payload `{ "fear_greed": {...}, "vix": {...} }`.
  - Explainability notes: include provider name, timestamp, and categorical interpretation text (e.g., "Extreme Fear").

- **Module Name**: `services/index_charts.py`
  - CLI invocation: `python -m services.index_charts --symbols ^GSPC,^IXIC,^DJI,BTC-USD,ETH-USD,SOL-USD --timeframe 1D`
  - Inputs: symbol list, timeframe.
  - Outputs: list of OHLCV arrays plus metadata.
  - Explainability notes: document candle interval, timezone normalization, fiat conversion rate for crypto, and gap-handling strategy.

- **Module Name**: `services/macro_boosters.py`
  - CLI invocation: `python -m services.macro_boosters --indicators ten_year_yield,breadth,macro_calendar`
  - Inputs: indicator list, provider credentials.
  - Outputs: structured indicators plus event arrays.
  - Explainability notes: cite formulas (e.g., breadth = count(symbols closing above 50DMA) / total) and note data staleness.

## Observability & Risk Controls *(describe monitoring + tests)*

- Logs: provider latency, cache hit ratio, error counts per source, calculation breadcrumbs for breadth.
- Metrics: time-to-render per widget, sentiment update freshness, percentage of successful refresh cycles.
- Golden datasets: store canned provider responses for `^GSPC` and sample macro events under `tests/fixtures/golden/market_sentiment/`.
- Contract tests: validate JSON schema for `MarketSentimentSnapshot`.
- Unit tests: verify candlestick transformations, breadth calculations, and caching TTL behavior.
- Integration tests: simulate provider outages ensuring stale indicators surface gracefully; run nightly via CI.
- Alerting: trigger pager when any provider error rate exceeds 10% for 15 minutes or when stale data exceeds TTL by >50%.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% of dashboard loads display current (≤2h old) fear/greed and VIX data within 3 seconds.
- **SC-002**: Index charts achieve ≥60 FPS interaction on modern browsers and refresh with new candles within 1 minute of availability.
- **SC-003**: Booster indicators (10Y yield, breadth, macro events) remain ≤24h old for trading days, with <5% fetch failure rate.
- **SC-004**: At least 80% of beta users report that the dashboard helps them assess market conditions faster than their prior setup.
