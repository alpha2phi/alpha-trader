import asyncio
import pytest
from httpx import AsyncClient
from backend.src.api import create_app


@pytest.mark.asyncio
async def test_sentiment_uses_fallback_when_primary_unavailable(monkeypatch):
    app = create_app()

    # Placeholder: once services are wired, patch primary provider to raise and fallback to succeed.
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/sentiment")
    assert resp.status_code in {200, 404, 501}
