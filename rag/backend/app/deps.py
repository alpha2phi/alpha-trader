from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    DEFAULT_CASH: float = 23080
    PER_TRADE_RISK_PCT: float = 0.05
    PORTFOLIO_USAGE_MIN: float = 0.30
    PORTFOLIO_USAGE_MAX: float = 0.40
    TOP25: str = "SPY,QQQ,IWM,VOO,.SPX,.XSP,TLT,GLD,XLE,XOP,SOXX,SOXL,AAPL,AMZN,MSFT,NVDA,TSLA,META,GOOGL,GOOG,NFLX,AMD,COST,UNH,LMT"
    VIX_AGGRESSIVE_THRESHOLD: float = 20
    VIX_DEFENSIVE_THRESHOLD: float = 15

    class Config:
        env_file = ".env"

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
