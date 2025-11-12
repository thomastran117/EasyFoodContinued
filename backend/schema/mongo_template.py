from __future__ import annotations
from typing import Optional, List
from datetime import datetime
import enum
from beanie import Document, Indexed, Link
from pydantic import Field, EmailStr


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


class Review(Document):
    user_id: int 
    restaurant: Link[Restaurant]
    description: str
    rating: float
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "reviews"


class Reservation(Document):
    user_id: int
    restaurant: Link[Restaurant]
    seats: int
    occasion: OccasionEnum
    details: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "reservations"


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
