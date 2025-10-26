from typing import Dict
from ..deps import get_settings

def per_trade_max_loss() -> float:
    s = get_settings()
    return s.DEFAULT_CASH * s.PER_TRADE_RISK_PCT

def within_portfolio_usage(current_usage:float) -> bool:
    s = get_settings()
    return s.PORTFOLIO_USAGE_MIN <= current_usage <= s.PORTFOLIO_USAGE_MAX

def credit_width_ok(credit:float, width:float) -> bool:
    return (credit / width) >= 0.33 - 1e-6

def vix_mode(vix:float) -> str:
    s = get_settings()
    if vix > s.VIX_AGGRESSIVE_THRESHOLD:
        return "aggressive"
    if vix < s.VIX_DEFENSIVE_THRESHOLD:
        return "defensive"
    return "balanced"
