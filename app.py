"""Fetch and display the trading accounts exposed by a moomoo OpenD instance."""
from __future__ import annotations

import ipaddress
import os
from numbers import Integral
from pathlib import Path
from typing import Callable, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent
DEFAULT_RSA_KEY_PATH = PROJECT_ROOT / "conn_key.txt"


def _load_moomoo_components() -> Tuple[object, ...]:
    """Import moomoo after pointing HOME to a writable path for its log files."""
    log_home = PROJECT_ROOT / ".moomoo_home"
    log_home.mkdir(parents=True, exist_ok=True)

    original_home = os.environ.get("HOME")
    os.environ["HOME"] = str(log_home)
    try:
        from moomoo import (
            OpenSecTradeContext,
            RET_OK,
            SecurityFirm,
            SysConfig,
            TrdAccStatus,
            TrdAccType,
            TrdEnv,
        )
    finally:
        if original_home is not None:
            os.environ["HOME"] = original_home
        else:
            os.environ.pop("HOME", None)

    return (
        OpenSecTradeContext,
        RET_OK,
        SecurityFirm,
        SysConfig,
        TrdAccStatus,
        TrdAccType,
        TrdEnv,
    )


(
    OpenSecTradeContext,
    RET_OK,
    SecurityFirm,
    SysConfig,
    TrdAccStatus,
    TrdAccType,
    TrdEnv,
) = _load_moomoo_components()


def _enum_to_string(value: object, mapper: Callable[[int], str]) -> str:
    if isinstance(value, Integral):
        return mapper(value)
    if isinstance(value, str):
        return value
    return "N/A" if value is None else str(value)


def _should_encrypt(host: str) -> bool:
    override = os.getenv("MOOMOO_FORCE_ENCRYPT")
    if override is not None:
        flag = override.strip().lower()
        return flag not in {"", "0", "false", "no"}

    try:
        ip_obj = ipaddress.ip_address(host)
        return not ip_obj.is_loopback
    except ValueError:
        return host.strip().lower() not in {"localhost"}


def _resolve_rsa_key_path() -> Optional[Path]:
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


def _configure_encryption(is_encrypt: bool) -> bool:
    if not is_encrypt:
        SysConfig.enable_proto_encrypt(False)
        return False

    rsa_path = _resolve_rsa_key_path()
    if rsa_path is None:
        raise RuntimeError(
            "Protocol encryption is required, but no RSA private key file was found. "
            "Set MOOMOO_RSA_KEY_PATH to the path of the key that matches your OpenD configuration."
        )

    SysConfig.enable_proto_encrypt(True)
    SysConfig.set_init_rsa_file(str(rsa_path))
    return True


def get_trading_accounts(host: str, port: int, is_encrypt: bool):
    trade_ctx: Optional[OpenSecTradeContext] = None
    try:
        trade_ctx = OpenSecTradeContext(host=host, port=port, is_encrypt=is_encrypt)
        ret_code, payload = trade_ctx.get_acc_list()
        if ret_code != RET_OK:
            raise RuntimeError(f"get_acc_list failed: {payload}")
        return payload
    finally:
        if trade_ctx is not None:
            trade_ctx.close()


def main() -> None:
    host = os.getenv("MOOMOO_OPEND_HOST", "127.0.0.1")
    port = int(os.getenv("MOOMOO_OPEND_PORT", "11111"))

    try:
        use_encryption = _configure_encryption(_should_encrypt(host))
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

    print("Trading accounts:\n")
    for record in accounts.to_dict(orient="records"):
        env = _enum_to_string(record.get("trd_env"), TrdEnv.to_string2)
        acc_type = _enum_to_string(record.get("acc_type"), TrdAccType.to_string2)
        status = _enum_to_string(record.get("acc_status"), TrdAccStatus.to_string2)
        firm = _enum_to_string(record.get("security_firm"), SecurityFirm.to_string2)
        markets = record.get("trdmarket_auth") or []
        markets_str = ", ".join(markets) if markets else "N/A"

        print(
            f"- env={env} | acc_id={record.get('acc_id')} | type={acc_type} | "
            f"status={status} | firm={firm} | markets={markets_str}"
        )


if __name__ == "__main__":
    main()
