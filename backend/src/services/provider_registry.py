from typing import List, Dict

# Provider priority order per signal; adjust when wiring real credentials.
PROVIDER_PRIORITY: Dict[str, List[str]] = {
    "sentiment": ["primary_sentiment", "secondary_sentiment"],
    "vix": ["primary_volatility", "secondary_volatility"],
    "index_ohlc": ["primary_index", "secondary_index"],
    "crypto_ohlc": ["primary_crypto", "secondary_crypto"],
    "ten_year_yield": ["primary_macro", "secondary_macro"],
    "breadth": ["primary_breadth", "secondary_breadth"],
    "macro_events": ["primary_calendar", "secondary_calendar"],
}


def get_priority(signal: str) -> List[str]:
    return PROVIDER_PRIORITY.get(signal, [])
