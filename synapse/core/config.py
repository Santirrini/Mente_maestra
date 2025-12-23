from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    HEARTBEAT_INTERVAL: int = 2  # Reduced for faster testing
    DEFAULT_STATE_TTL: Optional[int] = 3600
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
