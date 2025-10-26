from fastapi import APIRouter
from ..data.schemas import RunDailyRequest, RunDailyResponse
from ..services import screening
from ..services import retrieval
from ..services import tools
from ..services.formatting import short_premium_table, long_term_table

router = APIRouter(prefix="/run-daily", tags=["daily"])

@router.post("", response_model=RunDailyResponse)
def run_daily(payload: RunDailyRequest):
    # Short-premium candidates
    ideas = screening.screen_top_ideas(max_n=5)
    sp_md = short_premium_table(ideas)

    # Long-term buys placeholder
    long_term = []  # fill with (ticker, rationale, alloc)
    lt_md = long_term_table(long_term)

    notes = None
    # Optional: add a warning depending on VIX
    vix = tools.get_vix()
    notes = f"VIX: {vix} (defensive if <15, aggressive if >20)."

    return RunDailyResponse(short_premium_table_md=sp_md, long_term_table_md=lt_md, notes=notes)
