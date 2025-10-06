"""Formatting utilities for presenting moomoo trading data."""

from __future__ import annotations

import math
from numbers import Integral
from typing import Callable


def format_numeric(value: object, precision: int = 2) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, str):
        return value
    try:
        number = float(value)
    except (TypeError, ValueError):
        return "N/A"
    if math.isnan(number) or math.isinf(number):
        return "N/A"
    formatted = f"{number:.{precision}f}"
    if "." in formatted:
        formatted = formatted.rstrip("0").rstrip(".")
    return formatted


def format_quantity(value: object) -> str:
    if value is None:
        return "N/A"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if math.isnan(number) or math.isinf(number):
        return "N/A"
    if number.is_integer():
        return f"{int(number)}"
    return format_numeric(number, 2)


def format_percentage(value: object) -> str:
    numeric = format_numeric(value, 2)
    return f"{numeric}%" if numeric != "N/A" else numeric


def format_money(value: object) -> str:
    return format_numeric(value, 2)


def format_price(value: object) -> str:
    return format_numeric(value, 4)


def enum_to_string(value: object, mapper: Callable[[int], str]) -> str:
    if isinstance(value, Integral):
        return mapper(value)
    if isinstance(value, str):
        return value
    return "N/A" if value is None else str(value)
