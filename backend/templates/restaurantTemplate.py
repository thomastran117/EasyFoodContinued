from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from beanie import Document, Link
from pydantic import Field

from templates.categoryTemplate import Category
from templates.userTemplate import User


class Restaurant(Document):
    name: str
    description: str
    location: str
    logoUrl: str

    user: Optional[Link[User]] = None
    category: Optional[Link[Category]] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "restaurants"
        use_revision = False
