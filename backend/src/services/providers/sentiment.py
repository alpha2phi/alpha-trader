from typing import Any, Dict, Optional


class SentimentProviderClient:
    """Fetch Fear & Greed data."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def fetch(self) -> Dict[str, Any]:
        # TODO: implement real provider call
        raise NotImplementedError
