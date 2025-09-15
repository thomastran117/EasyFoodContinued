from pydantic_settings import BaseSettings
from typing import List, Optional
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

    email: Optional[str] = None
    password: Optional[str] = None

    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    google_redirect_uri: Optional[str] = None

    ms_tenant_id: Optional[str] = None
    ms_client_id: Optional[str] = None
    ms_client_secret: Optional[str] = None
    ms_redirect_uri: Optional[str] = None

    google_oauth_enabled: bool = False
    ms_oauth_enabled: bool = False
    email_enabled: bool = False

    @field_validator("database_url", "redis_url")
    def must_not_be_empty(cls, v, field):
        if not v:
            logger.error(f"The {field.name} is not set in .env")
            raise ValueError(f"The {field.name} is not set in .env")
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.google_oauth_enabled = all(
            [self.google_client_id, self.google_client_secret, self.google_redirect_uri]
        )

        self.ms_oauth_enabled = all(
            [
                self.ms_tenant_id,
                self.ms_client_id,
                self.ms_client_secret,
                self.ms_redirect_uri,
            ]
        )

        self.email_enabled = all([self.email, self.password])

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", ".env")
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
