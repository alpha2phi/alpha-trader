from fastapi import APIRouter
from ..services import retrieval, tools

router = APIRouter(prefix="/explain", tags=["explain"])

@router.post("/{ticker}")
def explain_ticker(ticker:str):
    # Return which rules/macro notes applied (stub)
    playbook = retrieval.fetch_playbook_chunks()
    ivr = tools.get_ivrank(ticker)
    tech = tools.get_technicals(ticker)
    return {
        "ticker": ticker.upper(),
        "rules": playbook,
        "snapshot": {"IVR": ivr, "RSI": tech["rsi"], "levels": f"{tech['support']} / {tech['resistance']}"}
    }
