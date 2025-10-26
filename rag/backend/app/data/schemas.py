from pydantic import BaseModel, Field
from typing import List, Optional

class ShortPremiumIdea(BaseModel):
    ticker: str
    strategy: str
    pop: Optional[float] = None
    max_profit: Optional[float] = None
    max_loss: Optional[float] = None
    notes: str

class RunDailyRequest(BaseModel):
    use_watchlist: bool = True

class RunDailyResponse(BaseModel):
    short_premium_table_md: str
    long_term_table_md: str
    notes: Optional[str] = None

class PaperTradeRequest(BaseModel):
    ticker: str
    strategy: str
    qty: int = 1

class ApproveOrderRequest(BaseModel):
    order_id: str
