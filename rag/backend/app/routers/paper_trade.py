from fastapi import APIRouter
from ..data.schemas import PaperTradeRequest

router = APIRouter(prefix="/paper-trade", tags=["paper"])

@router.post("")
def paper_trade(payload: PaperTradeRequest):
    # Stub: pretend we paper-traded and return an order id
    return {"order_id": "SIM-ORDER-001", "status": "accepted", "echo": payload.model_dump()}
