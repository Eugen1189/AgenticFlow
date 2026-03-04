from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """System settings and environment variables."""
    
    # API Keys
    OPENAI_API_KEY: str
    TAVILY_API_KEY: str
    
    # Application Configuration
    LOG_LEVEL: str = "INFO"
    APP_VERSION: str = "0.1.0"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
