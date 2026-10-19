from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App metadata
    PROJECT_NAME: str = "Production FastAPI Service"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Environment & runtime
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    DEBUG: bool = False

    # Server binding
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Application secrets & security
    SECRET_KEY: str = "insecure-fallback-secret-change-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Pydantic v2 configuration settings
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()