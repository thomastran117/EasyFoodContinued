from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional

from beanie import Document, Indexed, Link
from pydantic import EmailStr, Field


class OccasionEnum(str, enum.Enum):
    BIRTHDAY = "birthday"
    ANNIVERSARY = "anniversary"
    BUSINESS = "business"
    DATE = "date"
    OTHER = "other"


class Category(Document):
    name: Indexed(str, unique=True)
    description: Optional[str] = None

    class Settings:
        name = "categories"
        use_revision = False


class Restaurant(Document):
    name: str
    description: str
    location: str
    logoUrl: str

    owner_id: int
    category: Optional[Link[Category]] = None

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "restaurants"
        use_revision = False


class Food(Document):
    name: str
    description: str
    price: float
    imageUrl: str
    calories: Optional[float] = None
    tags: Optional[List[str]] = None
    ingredients: Optional[List[str]] = None

    restaurant: Link[Restaurant]

    class Settings:
        name = "foods"
        use_revision = False


class Review(Document):
    user_id: int  # stored in SQL
    restaurant: Link[Restaurant]
    description: str
    rating: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "reviews"
        use_revision = False


class Reservation(Document):
    user_id: int
    restaurant: Link[Restaurant]
    seats: int
    occasion: OccasionEnum
    details: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "reservations"
        use_revision = False


class Survey(Document):
    user_id: int
    question_one: str
    question_two: str
    question_three: str
    question_four: str
    rating: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "surveys"
        use_revision = False
