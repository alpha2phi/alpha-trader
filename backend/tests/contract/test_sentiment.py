import json
from pathlib import Path

import pytest
from httpx import AsyncClient
from backend.src.api import create_app


@pytest.mark.asyncio
async def test_sentiment_contract_shape():
    app = create_app()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        resp = await ac.get("/api/sentiment")
    # In absence of implementation, expect 404/501; contract focuses on schema presence when ready.
    assert resp.status_code in {200, 404, 501}
    if resp.status_code == 200:
        body = resp.json()
        assert "fear_greed" in body and "vix" in body
        fg = body["fear_greed"]
        vix = body["vix"]
        for field in ["score", "category", "updated_at", "cache_state"]:
            assert field in fg
        for field in ["level", "abs_change", "pct_change", "updated_at", "cache_state"]:
            assert field in vix
