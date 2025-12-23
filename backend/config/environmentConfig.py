import os
from typing import List, Optional

from pydantic import ConfigDict, field_validator
from pydantic_settings import BaseSettings

from utilities.logger import logger


class Settings(BaseSettings):
    mode: str = "development"
    redis_url: str
    mongo_url: str
    celery_broker_url: str
    celery_result_backend: str
    port: int = 8040
    model_config = ConfigDict(
        extra="ignore",
        env_file=os.path.join(os.path.dirname(__file__), "..", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        dotenv_override=False,
    )
    cors_allowed_region: List[str] = [
        "http://localhost:3040",
        "http://127.0.0.1:3040",
        "http://localhost:5173",
    ]

    secret_key: str = "default-key"
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

    paypal_mode: str = "sandbox"
    paypal_client_id: Optional[str] = None
    paypal_secret_key: Optional[str] = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.google_oauth_enabled = all([self.google_client_id])

        self.ms_oauth_enabled = all([self.ms_tenant_id, self.ms_client_id])

        self.email_enabled = all([self.email, self.password])

        self.recaptcha_enabled = all([self.google_secret_key])


settings = Settings()
