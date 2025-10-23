from typing import Annotated

from pydantic import BaseModel, Field


class ReviewCreateDto(BaseModel):
    name: str
    description: str
    rating: Annotated[float, Field(strict=True, ge=0, le=5)]


class ReviewUpdateDto(BaseModel):
    name: str | None = None
    description: str | None = None
    rating: Annotated[float, Field(strict=True, ge=0, le=5)] | None = None
