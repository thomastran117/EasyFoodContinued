from __future__ import annotations

import enum
from datetime import datetime
from typing import List, Optional

from beanie import Document, Indexed, Link
from pydantic import EmailStr, Field
from pymongo import IndexModel


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

    user_id: int
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
    user_id: int
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
                partialFilterExpression={"username": {"$exists": True, "$ne": None}},
            ),
            IndexModel(
                [("google_id", 1)],
                unique=True,
                partialFilterExpression={"google_id": {"$exists": True, "$ne": None}},
            ),
            IndexModel(
                [("microsoft_id", 1)],
                unique=True,
                partialFilterExpression={
                    "microsoft_id": {"$exists": True, "$ne": None}
                },
            ),
        ]
