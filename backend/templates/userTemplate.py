from __future__ import annotations

from datetime import datetime
from typing import Optional

from beanie import Document
from pydantic import EmailStr, Field
from pymongo import IndexModel


class User(Document):
    email: EmailStr
    username: Optional[str] = None

    password: Optional[str] = None
    role: str = Field(default="user")
    provider: str = Field(default="local")

    google_id: Optional[str] = None
    microsoft_id: Optional[str] = None

    name: Optional[str] = None
    avatar: Optional[str] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "users"
        indexes = [
            IndexModel(
                [("email", 1)],
                unique=True,
            ),
            IndexModel(
                [("username", 1)],
                unique=True,
                partialFilterExpression={
                    "username": {"$type": "string"}
                },
            ),
            IndexModel(
                [("google_id", 1)],
                unique=True,
                partialFilterExpression={
                    "google_id": {"$type": "string"}
                },
            ),
            IndexModel(
                [("microsoft_id", 1)],
                unique=True,
                partialFilterExpression={
                    "microsoft_id": {"$type": "string"}
                },
            ),
        ]
