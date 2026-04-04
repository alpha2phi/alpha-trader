import json
import time
from typing import Any, Optional

try:
    import redis  # type: ignore
except ImportError:  # pragma: no cover - redis may not be installed yet
    redis = None


class CacheClient:
    """Thin cache wrapper to store JSON-serializable data with TTL metadata."""

    def __init__(self, redis_url: str):
        if redis is None:
            raise RuntimeError("redis library is not installed")
        self._client = redis.Redis.from_url(redis_url, decode_responses=True)

    def set(self, key: str, value: Any, ttl_seconds: int) -> None:
        payload = json.dumps({"data": value, "written_at": time.time()})
        self._client.setex(key, ttl_seconds, payload)

    def get(self, key: str) -> tuple[Optional[Any], Optional[float]]:
        raw = self._client.get(key)
        if raw is None:
            return None, None
        decoded = json.loads(raw)
        return decoded.get("data"), decoded.get("written_at")


def is_stale(written_at: Optional[float], ttl_seconds: int) -> bool:
    if written_at is None:
        return True
    return (time.time() - written_at) > ttl_seconds
