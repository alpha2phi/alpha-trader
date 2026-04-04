from fastapi import FastAPI, APIRouter
from backend.src.api import sentiment


def create_app() -> FastAPI:
    """Create the FastAPI application with shared middleware and health check."""
    app = FastAPI(title="Market Sentiment Dashboard API")

    router = APIRouter()

    @router.get("/health", tags=["health"])
    async def health() -> dict:
        return {"status": "ok"}

    app.include_router(router)
    app.include_router(sentiment.router)
    return app


app = create_app()
