import os
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "80db566585160766979-4816e409ec86731")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://satenhance:satenhance@localhost:5432/satenhance"
    )

    SQLALCHEMY_DATABASE_URI: str = DATABASE_URL

    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    class Config:
        case_sensitive = True


settings = Settings()
