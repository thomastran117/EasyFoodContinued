from __future__ import annotations

from typing import Optional

from beanie import Document, Indexed


class Category(Document):
    name: Indexed(str, unique=True)
    description: Optional[str] = None

    class Settings:
        name = "categories"
        use_revision = False
