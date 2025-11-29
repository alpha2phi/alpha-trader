 # alpha-trader 🚀

A dashboard to analyze stocks using fundamental, technical, sentiment analysis and AI insights.


## speckit

### clarify

/speckit.clarify
Goal: I need clarification on the "001-market-sentiment-dashboard" requirements.
Checklist: specs/001-market-sentiment-dashboard/checklists/requirements.md
Ask: Identify unclear or ambiguous items, missing success criteria, dependencies, and edge cases. Propose pointed questions to the stakeholder to resolve them. Keep it concise and actionable.

Please read specs/001-market-sentiment-dashboard/checklists/requirements.md and draft concise clarification questions for any ambiguous requirements, missing acceptance criteria, external dependencies (APIs/data sources), and edge cases. Return the questions grouped by topic (data, UI/UX, performance, rollout/testing).

Read the review and acceptance checklist, and check off each item in the checklist if the feature spec meets the criteria. Leave it empty if it does not.

### plan

/speckit.plan
Goal: Plan the Market Sentiment Dashboard implementation using Next.js (React + TS) frontend, FastAPI backend, Redis cache, Postgres provenance store, and Celery/APScheduler jobs, matching the requirements in requirements.md and specs/001-market-sentiment-dashboard/spec.md.

Key scope:
- Sentiment snapshot: Fear & Greed + VIX with freshness, stale indicators, per-card retries.
- Cross-market candles: S&P 500, Nasdaq, Dow, BTC, ETH, SOL with 1D/1W/1M toggles, per-symbol freshness, cached fallback.
- Boosters: 10Y yield, breadth, macro events (2-week window), per-card retries, cache TTLs.
- Shared market_data_service with single caching layer, provenance storage under data/provenance/market-sentiment/.
- Observability: metrics for latency/cache hits/error counts/stale serves; golden fixtures in tests/fixtures/golden/market_sentiment/.

Ask:
/speckit.plan please produce a delivery plan with milestones, swimlanes, and test strategy aligned to the above stack and requirements. Include sequencing for API clients, caching layer, UI cards/charts, retries/stale states, scheduled jobs per cadence (15m candles, 2h sentiment, 24h boosters), and CI tests (contract/unit/integration). Keep it concise and actionable.
