import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv(".env")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

class Settings(BaseSettings):
    ALGORITHM: str
    DATABASE_URL: str

    class config:
       env_file = ".env"

Settings = Settings()