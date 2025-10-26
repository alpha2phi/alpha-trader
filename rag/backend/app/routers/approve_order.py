from fastapi import APIRouter
from ..data.schemas import ApproveOrderRequest

router = APIRouter(prefix="/approve-order", tags=["orders"])

@router.post("")
def approve(payload: ApproveOrderRequest):
    # Stub: in real life call broker to place the order
    return {"order_id": payload.order_id, "status": "sent_to_broker"}
