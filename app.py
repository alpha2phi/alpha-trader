"""Fetch and display US trading positions exposed by a moomoo OpenD instance."""

from __future__ import annotations

import os

from formatting import (
    enum_to_string,
    format_money,
    format_percentage,
    format_price,
    format_quantity,
)
from moomoo_helpers import (
    TrdEnv,
    configure_encryption,
    get_account_positions,
    get_trading_accounts,
    should_encrypt,
)


def main() -> None:
    host = os.getenv("MOOMOO_OPEND_HOST", "127.0.0.1")
    port = int(os.getenv("MOOMOO_OPEND_PORT", "11111"))

    try:
        use_encryption = configure_encryption(should_encrypt(host))
    except Exception as exc:
        print(f"Failed to configure encryption: {exc}")
        return

    try:
        accounts = get_trading_accounts(host, port, use_encryption)
    except Exception as exc:
        print(f"Failed to retrieve trading accounts: {exc}")
        return

    if accounts.empty:
        print("No trading accounts returned by OpenD.")
        return

    try:
        positions_by_account = get_account_positions(
            host, port, use_encryption, accounts)
    except Exception as exc:
        print(f"Failed to retrieve account positions: {exc}")
        return

    print("Positions:\n")
    any_positions = False

    for record in accounts.to_dict(orient="records"):
        env = enum_to_string(record.get("trd_env"), TrdEnv.to_string2)
        acc_id_value = record.get("acc_id")
        try:
            acc_id_key = int(acc_id_value)
        except (TypeError, ValueError):
            acc_id_key = None

        print(f"Account {acc_id_value} ({env}):")
        if acc_id_key is None:
            print("  Unable to determine account identifier.")
            continue

        positions_df = positions_by_account.get(acc_id_key)
        if positions_df is None:
            print("  Unable to load US positions for this account.")
            continue

        if positions_df.empty:
            print("  No US positions.")
            continue

        any_positions = True
        for position in positions_df.to_dict(orient="records"):
            code = position.get("code") or "N/A"
            side = position.get("position_side") or "N/A"
            qty = format_quantity(position.get("qty"))
            avg_cost = format_price(position.get("average_cost"))
            market_val = format_money(position.get("market_val"))
            pl_val = format_money(position.get("pl_val"))
            pl_pct = format_percentage(position.get("pl_ratio"))

            print(
                f"  - {code} ({side}) | qty={qty} | cost={avg_cost} | "
                f"mv={market_val} | pl={pl_val} | pl%={pl_pct}"
            )

    if not any_positions:
        print("No US positions across all accounts.")


if __name__ == "__main__":
    main()
