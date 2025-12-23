from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    REDIS_URL: str = "redis://localhost:6379/0"
    HEARTBEAT_INTERVAL: float = 5.0
    DEFAULT_STATE_TTL: int = 3600 # 1 hour
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()