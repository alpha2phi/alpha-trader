# Tool layer for market data & options. Replace stubs with real API logic.
# If API keys are not present, functions will fall back to mock data.
from typing import List, Dict, Any, Optional
import os, math, time
import httpx
import pandas as pd

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
TRADIER_TOKEN = os.getenv("TRADIER_TOKEN")
TOP25_DEFAULT = os.getenv("TOP25","SPY,QQQ,IWM,VOO,.SPX,.XSP,TLT,GLD,XLE,XOP,SOXX,SOXL,AAPL,AMZN,MSFT,NVDA,TSLA,META,GOOGL,GOOG,NFLX,AMD,COST,UNH,LMT").split(",")

# ----------------- Watchlist -----------------
def get_watchlist(path:str="../data/watchlist.csv") -> List[str]:
    if os.path.exists(path):
        try:
            s = pd.read_csv(path)
            if s.shape[1] >= 1:
                return [str(x).strip().upper() for x in s.iloc[:,0].dropna().tolist()]
        except Exception:
            pass
    return TOP25_DEFAULT

# ----------------- Market regime -----------------
def get_vix() -> float:
    # Polygon has VIX via ^VIX (indices); Tradier also provides quotes. Use mock if no key.
    if POLYGON_API_KEY:
        try:
            # NOTE: Replace with your preferred data source endpoint. This is a placeholder.
            # polygon reference: /v2/aggs/ticker/C:VIX/prev - requires proper ticker mapping
            return 18.7
        except Exception:
            pass
    return 18.0

# ----------------- Earnings -----------------
def get_earnings(ticker:str) -> Optional[str]:
    # Use a fundamentals provider (Polygon, FMP) – returning None if unknown.
    return None

# ----------------- IV Rank -----------------
def get_ivrank(ticker:str) -> Optional[float]:
    # True IVR requires historical IV. Stub below; replace with your own pipeline.
    mock = {"SPY":55, "QQQ":48, "IWM":60, "AAPL":52, "NVDA":65, "TSLA":58}
    return mock.get(ticker, 50.0)

# ----------------- Liquidity -----------------
def get_liquidity_score(ticker:str) -> float:
    # Combine spread % + OI quality. Placeholder returns high liquidity for index/megacaps.
    liquid = {"SPY":0.98,"QQQ":0.96,"IWM":0.93,"AAPL":0.92,"NVDA":0.9,"TSLA":0.9}
    return liquid.get(ticker, 0.8)

# ----------------- Technicals -----------------
def get_technicals(ticker:str) -> Dict[str, Any]:
    # Stub; replace with your TA pipeline (RSI/levels/ATR).
    return {"rsi": 45, "support": "near 50DMA", "resistance": "recent swing high"}

# ----------------- Options Chains -----------------
def _tradier_chain(ticker:str, expiry:Optional[str]=None) -> Dict[str, Any]:
    if not TRADIER_TOKEN:
        return {"contracts":[{"strike":100,"delta":-0.25,"bid":1.9,"ask":2.0},{"strike":95,"delta":-0.15,"bid":1.2,"ask":1.3}]}
    try:
        headers = {"Authorization": f"Bearer {TRADIER_TOKEN}","Accept":"application/json"}
        params = {"symbol": ticker, "greeks":"true"}
        if expiry: params["expiration"] = expiry
        url = "https://api.tradier.com/v1/markets/options/chains"
        with httpx.Client(timeout=10) as c:
            r = c.get(url, headers=headers, params=params)
            r.raise_for_status()
            return r.json()
    except Exception:
        return {"contracts":[{"strike":100,"delta":-0.25,"bid":1.9,"ask":2.0},{"strike":95,"delta":-0.15,"bid":1.2,"ask":1.3}]}

def _polygon_chain_placeholder(ticker:str, dte:int=45) -> Dict[str, Any]:
    # Polygon options aggregates live behind authenticated endpoints – stub for now.
    return {"dte": dte, "contracts":[{"strike":100,"delta":-0.25,"mid":1.8},{"strike":95,"delta":-0.15,"mid":1.1}]}

def get_chain(ticker:str, dte:int=45) -> Dict[str, Any]:
    # For demo, synthesize a 5-wide vertical near 0.25Δ with ~1.8 credit.
    return {"dte": dte, "short_delta": 0.25, "width": 5.0, "credit": 1.8}

# ----------------- Simulators -----------------
def simulate_vertical_put(width:float, credit:float) -> Dict[str, float]:
    max_profit = credit * 100
    max_loss = (width - credit) * 100
    pop = 70.0  # delta proxy placeholder
    return {"max_profit": max_profit, "max_loss": max_loss, "pop": pop}

def simulate_vertical_call(width:float, credit:float) -> Dict[str, float]:
    max_profit = credit * 100
    max_loss = (width - credit) * 100
    pop = 70.0
    return {"max_profit": max_profit, "max_loss": max_loss, "pop": pop}
