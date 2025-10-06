"""MoMo OpenAPI helper functions for contexts, encryption, and positions."""

from __future__ import annotations

import ipaddress
import os
from pathlib import Path
from typing import Dict, Optional

from .config import DEFAULT_RSA_KEY_PATH 

from moomoo import (
OpenSecTradeContext,
RET_OK,
SysConfig,
TrdMarket,
TrdEnv,
)


def normalize_trd_env(value: object) -> Optional[str]:
    if isinstance(value, str):
        return value if TrdEnv.if_has_key(value) else None
    if isinstance(value, int):
        label = TrdEnv.to_string2(value)
        return label if TrdEnv.if_has_key(label) else None
    return None


def should_encrypt(host: str) -> bool:
    override = os.getenv("MOOMOO_FORCE_ENCRYPT")
    if override is not None:
        flag = override.strip().lower()
        return flag not in {"", "0", "false", "no"}

    try:
        ip_obj = ipaddress.ip_address(host)
        return not ip_obj.is_loopback
    except ValueError:
        return host.strip().lower() not in {"localhost"}


def resolve_rsa_key_path() -> Optional[Path]:
    candidates = []
    env_path = os.getenv("MOOMOO_RSA_KEY_PATH")
    if env_path:
        candidates.append(Path(env_path).expanduser())

    candidates.append(DEFAULT_RSA_KEY_PATH)

    home_value = os.environ.get("HOME")
    if home_value:
        home_dir = Path(home_value).expanduser()
        candidates.append(home_dir / "conn_key.txt")
        candidates.append(home_dir / ".com.moomoo.OpenD" / "conn_key.txt")

    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    return None


def configure_encryption(is_encrypt: bool) -> bool:
    if not is_encrypt:
        SysConfig.enable_proto_encrypt(False)
        return False

    rsa_path = resolve_rsa_key_path()
    if rsa_path is None:
        raise RuntimeError(
            "Protocol encryption is required, but no RSA private key file was found. "
            "Set MOOMOO_RSA_KEY_PATH to the path of the key that matches your OpenD configuration."
        )

    SysConfig.enable_proto_encrypt(True)
    SysConfig.set_init_rsa_file(str(rsa_path))
    return True


def unlock_trade_context(trade_ctx: OpenSecTradeContext) -> None:
    password = get_trading_password()
    if not password:
        return
    ret_code, payload = trade_ctx.unlock_trade(password=password)
    if ret_code != RET_OK:
        raise RuntimeError(f"unlock_trade failed: {payload}")


def get_positions(
    trade_ctx: OpenSecTradeContext,
    acc_id: int,
    trd_env: str = TrdEnv.REAL,
    position_market: str = TrdMarket.US,
    refresh_cache: bool = True,
):
    ret_code, payload = trade_ctx.position_list_query(
        trd_env=trd_env,
        acc_id=acc_id,
        position_market=position_market,
        refresh_cache=refresh_cache,
    )
    if ret_code != RET_OK:
        raise RuntimeError(
            f"position_list_query failed for account {acc_id}: {payload}"
        )
    return payload


def get_trading_accounts(host: str, port: int, is_encrypt: bool):
    trade_ctx: Optional[OpenSecTradeContext] = None
    try:
        trade_ctx = OpenSecTradeContext(
            filter_trdmarket=TrdMarket.US, host=host, port=port, is_encrypt=is_encrypt
        )
        ret_code, accounts = trade_ctx.get_acc_list()
        if ret_code != RET_OK:
            raise RuntimeError(f"get_acc_list failed: {accounts}")
        return accounts
    finally:
        if trade_ctx is not None:
            trade_ctx.close()


def get_account_positions(
    host: str,
    port: int,
    is_encrypt: bool,
    accounts,
    position_market: str = TrdMarket.US,
    refresh_cache: bool = True,
) -> Dict[int, object]:
    trade_ctx: Optional[OpenSecTradeContext] = None
    try:
        trade_ctx = OpenSecTradeContext(
            filter_trdmarket=position_market, host=host, port=port, is_encrypt=is_encrypt
        )
        unlock_trade_context(trade_ctx)
        positions: Dict[int, object] = {}
        for record in accounts.to_dict(orient="records"):
            acc_id_raw = record.get("acc_id")
            try:
                acc_id = int(acc_id_raw)
            except (TypeError, ValueError):
                continue

            trd_env_label = normalize_trd_env(record.get("trd_env"))
            if trd_env_label is None:
                positions[acc_id] = None
                continue

            positions[acc_id] = get_positions(
                trade_ctx,
                acc_id,
                trd_env=trd_env_label,
                position_market=position_market,
                refresh_cache=refresh_cache,
            )
        return positions
    finally:
        if trade_ctx is not None:
            trade_ctx.close()

def get_trading_password() -> str:
    """Return the trade password to unlock live accounts."""
    value = os.getenv("MOOMOO_TRADE_PASSWORD", "")
    if isinstance(value, str):
        value = value.strip()
    return value if value else ""