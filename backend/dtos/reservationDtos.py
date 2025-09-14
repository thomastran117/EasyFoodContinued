from pydantic import BaseModel, Field
from typing import Annotated
import enum


class OccasionEnum(str, enum.Enum):
    BIRTHDAY = "birthday"
    ANNIVERSARY = "anniversary"
    BUSINESS = "business"
    DATE = "date"
    OTHER = "other"


class ReservationCreateDto(BaseModel):
    seats: Annotated[int, Field(strict=True, gt=0)]
    occasion: OccasionEnum
    details: str


class ReservationUpdateDto(BaseModel):
    seats: Annotated[int, Field(strict=True, gt=0)]
    occasion: OccasionEnum | None = None
    details: str | None = None
