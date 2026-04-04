from fastapi import APIRouter, HTTPException

from backend.src.models.market import MarketSentimentSnapshot
from backend.src.services.cache import CacheClient
from backend.src.services.config import get_settings
from backend.src.services.sentiment_service import SentimentService

router = APIRouter(prefix="/api", tags=["sentiment"])


@router.get("/sentiment", response_model=MarketSentimentSnapshot)
def get_sentiment():
    settings = get_settings()
    cache = CacheClient(settings.redis_url)
    service = SentimentService(cache=cache)
    try:
        return service.get_snapshot()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))
