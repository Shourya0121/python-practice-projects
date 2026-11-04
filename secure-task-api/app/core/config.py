
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3308
    MYSQL_DATABASE: str = "secure_task_db"
    MYSQL_USER: str = "secure_task_user"
    MYSQL_PASSWORD: str = "your-existing-password"

    TEST_MYSQL_DATABASE: str = "secure_task_test_db"

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()

