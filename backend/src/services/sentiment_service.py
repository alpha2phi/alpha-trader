from datetime import datetime, timezone
from typing import Any, Dict

from backend.src.models.market import MarketSentimentSnapshot, FearGreed, VixReading
from backend.src.services.cache import CacheClient, is_stale
from backend.src.services.config import get_settings
from backend.src.services.provenance import record_provenance
from backend.src.services.provider_registry import get_priority
from backend.src.services.providers.sentiment import SentimentProviderClient
from backend.src.services.providers.volatility import VolatilityProviderClient


class SentimentService:
    def __init__(self, cache: CacheClient):
        settings = get_settings()
        self.cache = cache
        self.ttl = settings.cache_ttl_sentiment_seconds
        self.provenance_dir = settings.postgres_dsn  # will pass into record_provenance
        self.postgres_dsn = settings.postgres_dsn
        self.sentiment_clients = [SentimentProviderClient(settings.sentiment_api_key)]
        self.vix_clients = [VolatilityProviderClient(settings.market_data_api_key)]

    def _select_first(self, clients):
        for client in clients:
            try:
                return client.fetch()
            except Exception:
                continue
        raise RuntimeError("All providers failed")

    def get_snapshot(self) -> MarketSentimentSnapshot:
        cache_key = "sentiment_snapshot"
        cached, written_at = self.cache.get(cache_key)
        settings = get_settings()
        if cached:
            stale = is_stale(written_at, self.ttl)
            payload = cached
            fg = payload["fear_greed"]
            vix = payload["vix"]
            return MarketSentimentSnapshot(
                fear_greed=FearGreed(
                    score=fg["score"],
                    category=fg["category"],
                    updated_at=datetime.fromtimestamp(fg["updated_at"], tz=timezone.utc),
                    cache_state="stale" if stale else "fresh",
                    provider=fg.get("provider"),
                ),
                vix=VixReading(
                    level=vix["level"],
                    abs_change=vix["abs_change"],
                    pct_change=vix["pct_change"],
                    updated_at=datetime.fromtimestamp(vix["updated_at"], tz=timezone.utc),
                    cache_state="stale" if stale else "fresh",
                    provider=vix.get("provider"),
                ),
            )

        fg_raw = self._select_first(self.sentiment_clients)
        vix_raw = self._select_first(self.vix_clients)
        fg_payload = {
            "score": fg_raw.get("score", 0),
            "category": fg_raw.get("category", "unknown"),
            "updated_at": datetime.now(tz=timezone.utc).timestamp(),
            "provider": fg_raw.get("provider"),
        }
        vix_payload = {
            "level": vix_raw.get("level", 0.0),
            "abs_change": vix_raw.get("abs_change", 0.0),
            "pct_change": vix_raw.get("pct_change", 0.0),
            "updated_at": datetime.now(tz=timezone.utc).timestamp(),
            "provider": vix_raw.get("provider"),
        }
        payload: Dict[str, Any] = {"fear_greed": fg_payload, "vix": vix_payload}
        self.cache.set(cache_key, payload, self.ttl)
        record_provenance(
            source="sentiment_snapshot",
            payload=payload,
            cache_key=cache_key,
            storage_dir=settings.__config__.path("data/provenance/market-sentiment"),  # type: ignore
            postgres_dsn=self.postgres_dsn,
        )
        return self.get_snapshot()
