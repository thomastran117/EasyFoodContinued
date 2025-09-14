from pydantic_settings import BaseSettings
from typing import List
from pydantic import field_validator
import os
from utilities.logger import get_logger

logger = get_logger(__name__)


class Settings(BaseSettings):
    database_url: str
    redis_url: str
    port: int = 8090

    cors_allowed_region: List[str] = [
        "http://localhost:3090",
        "http://127.0.0.1:3090",
        "http://localhost:5173",
    ]

    secret_key: str = "default-key"
    algorithm: str = "HS256"
    expire_minutes: int = 360

    email: str
    password: str

    google_client_id: str
    google_client_secret: str
    google_redirect_uri: str

    ms_tenant_id: str
    ms_client_id: str
    ms_client_secret: str
    ms_redirect_uri: str

    @field_validator("database_url", "redis_url")
    def must_not_be_empty(cls, v, field):
        if not v:
            raise ValueError(
                logger.error("The database or redis url is not set in .env")
            )
        return v

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
