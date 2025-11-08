import os
from typing import List, Optional

from pydantic import field_validator, ConfigDict
from pydantic_settings import BaseSettings

from utilities.logger import logger

class Settings(BaseSettings):
    database_url: str
    redis_url: str
    mongo_url: str
    port: int = 8090
    model_config = ConfigDict(
        extra="ignore",
        env_file=os.path.join(os.path.dirname(__file__), "..", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
    )    
    cors_allowed_region: List[str] = [
        "http://localhost:3050",
        "http://127.0.0.1:3050",
        "http://localhost:5173",
    ]

    jwt_secret_access: str = "default-key"
    jwt_secret_refresh: str = "default-key"
    jwt_secret_verify: str = "default-key"
    algorithm: str = "HS256"

    email: Optional[str] = None
    password: Optional[str] = None

    google_client_id: Optional[str] = None
    google_secret_key: Optional[str] = None

    ms_tenant_id: Optional[str] = None
    ms_client_id: Optional[str] = None

    google_oauth_enabled: bool = False
    ms_oauth_enabled: bool = False
    email_enabled: bool = False
    recaptcha_enabled: bool = False

    @field_validator("database_url", "redis_url")
    def must_not_be_empty(cls, v, field):
        if not v:
            logger.error(f"The {field.name} is not set in .env")
            raise ValueError(f"The {field.name} is not set in .env")
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.google_oauth_enabled = all([self.google_client_id])

        self.ms_oauth_enabled = all([self.ms_tenant_id, self.ms_client_id])

        self.email_enabled = all([self.email, self.password])

        self.recaptcha_enabled = all([self.google_secret_key])

settings = Settings()
