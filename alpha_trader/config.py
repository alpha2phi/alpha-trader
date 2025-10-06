"""Shared configuration and environment helpers for the alpha-trader CLI."""

from __future__ import annotations

import os
from pathlib import Path

_DOTENV_LOADED = False
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RSA_KEY_PATH = PROJECT_ROOT / "conn_key.txt"
ENV_FILE_PATH = PROJECT_ROOT / ".env"


def _load_env_file() -> None:
    """Populate ``os.environ`` with values from ``.env`` (first run only)."""
    global _DOTENV_LOADED
    if _DOTENV_LOADED:
        return

    _DOTENV_LOADED = True
    if not ENV_FILE_PATH.exists():
        return

    try:
        raw_lines = ENV_FILE_PATH.read_text(encoding="utf-8").splitlines()
    except OSError:
        return

    for raw_line in raw_lines:
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")):
            value = value[1:-1]

        if key and key not in os.environ:
            os.environ[key] = value


_load_env_file()
