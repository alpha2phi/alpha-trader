from functools import lru_cache
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    sentiment_api_key: str | None = Field(default=None, env="SENTIMENT_API_KEY")
    market_data_api_key: str | None = Field(default=None, env="MARKET_DATA_API_KEY")
    macro_data_api_key: str | None = Field(default=None, env="MACRO_DATA_API_KEY")
    redis_url: str = Field(default="redis://localhost:6379/0", env="REDIS_URL")
    postgres_dsn: str = Field(default="postgresql://user:pass@localhost:5432/alpha_trader", env="POSTGRES_DSN")
    cache_ttl_sentiment_seconds: int = Field(default=7200, env="CACHE_TTL_SENTIMENT_SECONDS")
    cache_ttl_candles_seconds: int = Field(default=900, env="CACHE_TTL_CANDLES_SECONDS")
    cache_ttl_boosters_seconds: int = Field(default=86400, env="CACHE_TTL_BOOSTERS_SECONDS")

    class Config:
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
