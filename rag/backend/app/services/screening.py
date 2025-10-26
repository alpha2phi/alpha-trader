from typing import List
from ..services import tools, risk, retrieval
from ..data.schemas import ShortPremiumIdea

TOP25 = tools.get_watchlist(path="../data/watchlist.csv")  # falls back to default list

def passes_filters(ticker:str) -> dict:
    ivr = tools.get_ivrank(ticker) or 0
    earn = tools.get_earnings(ticker)
    liq = tools.get_liquidity_score(ticker)
    tech = tools.get_technicals(ticker)
    ok = ivr >= 50 and earn is None and liq >= 0.7
    reason = {
        "IVR": ivr, "Earnings": earn or "none", "Liquidity": liq,
        "RSI": tech["rsi"], "Support/Resistance": f"{tech['support']}/{tech['resistance']}"
    }
    return {"ok": ok, "reason": reason}

def build_candidate(ticker:str) -> ShortPremiumIdea:
    ch = tools.get_chain(ticker, dte=45)
    credit = ch["credit"]
    width = ch["width"]
    # choose bullish put or bearish call based on RSI
    rsi = tools.get_technicals(ticker)["rsi"]
    if rsi < 35:
        strategy = f"Sell {ticker} {width}-wide Put Spread 45 DTE (~0.25Δ)"
        sim = tools.simulate_vertical_put(width=width, credit=credit)
    elif rsi > 65:
        strategy = f"Sell {ticker} {width}-wide Call Spread 45 DTE (~0.25Δ)"
        sim = tools.simulate_vertical_call(width=width, credit=credit)
    else:
        # neutral: default to put spread for demo
        strategy = f"Sell {ticker} {width}-wide Put Spread 45 DTE (~0.25Δ)"
        sim = tools.simulate_vertical_put(width=width, credit=credit)

    notes = f"IVR: {tools.get_ivrank(ticker)} | RSI: {rsi} | Support/Resistance: {tools.get_technicals(ticker)['support']}/{tools.get_technicals(ticker)['resistance']} | Fundamentals: N/A"
    return ShortPremiumIdea(
        ticker=ticker, strategy=strategy, pop=sim["pop"],
        max_profit=sim["max_profit"], max_loss=sim["max_loss"], notes=notes
    )

def screen_top_ideas(max_n:int=5) -> List[ShortPremiumIdea]:
    vix = tools.get_vix()
    _ = retrieval.fetch_macro_notes()  # hook for veto
    ideas: List[ShortPremiumIdea] = []
    for t in TOP25:
        f = passes_filters(t)
        if not f["ok"]:
            continue
        ch = tools.get_chain(t, dte=45)
        if not risk.credit_width_ok(credit=ch["credit"], width=ch["width"]):
            continue
        ideas.append(build_candidate(t))
        if len(ideas) >= max_n:
            break
    return ideas
