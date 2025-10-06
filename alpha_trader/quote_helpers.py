"""Quote-context helpers for retrieving user watchlists via moomoo OpenAPI."""

from __future__ import annotations

from typing import Dict, List, Tuple

from moomoo import OpenQuoteContext, RET_OK

from .moomoo_helpers import should_encrypt


def get_watchlist_groups(quote_ctx: "OpenQuoteContext") -> List[Dict[str, object]]:
    ret_code, df = quote_ctx.get_user_security_group()
    if ret_code != RET_OK:
        raise RuntimeError(f"get_user_security_group failed: {df}")
    return df.to_dict(orient="records")


def get_watchlist_securities(
    quote_ctx: "OpenQuoteContext", group_id: int
) -> List[Dict[str, object]]:
    ret_code, df = quote_ctx.get_user_security(group_id)
    if ret_code != RET_OK:
        raise RuntimeError(
            f"get_user_security failed for group {group_id}: {df}")
    return df.to_dict(orient="records")


def fetch_watchlists(host: str, port: int) -> List[Tuple[Dict[str, object], List[Dict[str, object]]]]:
    quote_ctx: OpenQuoteContext | None = None
    try:
        quote_ctx = OpenQuoteContext(
            host=host, port=port, is_encrypt=should_encrypt(host))
        groups = get_watchlist_groups(quote_ctx)
        results: List[Tuple[Dict[str, object], List[Dict[str, object]]]] = []
        for group in groups:
            group_id = group.get("id")
            if group_id is None:
                continue
            securities = get_watchlist_securities(quote_ctx, int(group_id))
            results.append((group, securities))
        return results
    finally:
        if quote_ctx is not None:
            quote_ctx.close()
