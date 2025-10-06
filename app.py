"""Fetch and display US trading positions exposed by a moomoo OpenD instance."""

from __future__ import annotations

import os

from alpha_trader.moomoo_helpers import (
    configure_encryption,
    should_encrypt,
)
from alpha_trader.quote_helpers import fetch_watchlists


def main() -> None:
    host = os.getenv("MOOMOO_OPEND_HOST", "127.0.0.1")
    port = int(os.getenv("MOOMOO_OPEND_PORT", "11111"))

    try:
        use_encryption = configure_encryption(should_encrypt(host))
    except Exception as exc:
        print(f"Failed to configure encryption: {exc}")
        return
    try:
        watchlists = fetch_watchlists(host, port)
    except Exception as exc:
        print(f"Failed to retrieve watchlists: {exc}")
        return

    if not watchlists:
        print("\nNo watchlists found.\n")
    else:
        print("\nWatchlists:\n")
        for group, securities in watchlists:
            list_name = group.get("name") or group.get(
                "group_name") or "Unnamed Group"
            print(f"- {list_name} ({len(securities)} items)")
            for item in securities:
                code = item.get("code") or "N/A"
                display = item.get("name") or item.get("stock_name") or "N/A"
                print(f"  - {code} {display}")


if __name__ == "__main__":
    main()
