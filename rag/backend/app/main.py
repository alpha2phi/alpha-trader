from fastapi import FastAPI
from .routers import run_daily, explain, paper_trade, approve_order

app = FastAPI(title="RAG Options Trader")

app.include_router(run_daily.router)
app.include_router(explain.router)
app.include_router(paper_trade.router)
app.include_router(approve_order.router)

@app.get("/health")
def health():
    return {"ok": True}
