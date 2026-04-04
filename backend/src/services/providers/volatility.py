from typing import Any, Dict, Optional


class VolatilityProviderClient:
    """Fetch VIX data."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key

    def fetch(self) -> Dict[str, Any]:
        # TODO: implement real provider call
        raise NotImplementedError
