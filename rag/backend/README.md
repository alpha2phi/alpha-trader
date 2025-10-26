# RAG Options Trader (Scaffold)

FastAPI backend that follows a tastytrade-style, short-premium workflow with RAG retrieval and tool-based numerics.

## Quickstart

1. **Python env**
   ```bash
   cd backend
   python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   cp app/.env.example app/.env  # update keys if needed
   ```

2. **Run API**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Try endpoints**
   - Swagger UI: http://localhost:8000/docs
   - `POST /run-daily`
   - `POST /explain/{ticker}`
   - `POST /paper-trade`
   - `POST /approve-order`

4. **Data**
   - Put your `watchlist.csv` in `data/watchlist.csv` (a sample is provided).
   - Add your market data pipelines under `scripts/` and wire them to `services/tools.py` functions.

## What you get

- **Strict tools-first numerics** (prices/IVR/greeks pulled by tool functions).
- **Tastytrade-style screen**: IVR filter, ~45 DTE, ~0.25 short-delta, ≥33% credit/width, earnings window exclusion, liquidity checks.
- **Risk guardrails**: per-trade max loss (~5% of $23,080), portfolio usage cap (30–40%), macro veto hooks.
- **RAG entry points** for your playbooks/macro notes (plug your vector DB in `services/retrieval.py`).

## Next steps

- Implement real data in `services/tools.py` (Polygon/IEX/Tradier/IBKR/Tastytrade).
- Implement your vector DB in `services/retrieval.py` (Qdrant/Weaviate/PGVector).
- Extend `scripts/ingest_example.py` to populate daily snapshots.



# Backend (FastAPI)

## Env
Copy `.env.example` to `.env` and add keys if you have them:

```
DEFAULT_CASH=23080
PER_TRADE_RISK_PCT=0.05
PORTFOLIO_USAGE_MIN=0.30
PORTFOLIO_USAGE_MAX=0.40
TOP25="SPY,QQQ,IWM,VOO,.SPX,.XSP,TLT,GLD,XLE,XOP,SOXX,SOXL,AAPL,AMZN,MSFT,NVDA,TSLA,META,GOOGL,GOOG,NFLX,AMD,COST,UNH,LMT"
VIX_AGGRESSIVE_THRESHOLD=20
VIX_DEFENSIVE_THRESHOLD=15

# Optional external providers
POLYGON_API_KEY=your_polygon_key
TRADIER_TOKEN=your_tradier_token
```
