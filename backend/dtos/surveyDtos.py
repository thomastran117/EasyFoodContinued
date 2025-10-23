from typing import Annotated

from pydantic import BaseModel, Field


class SurveyCreateDto(BaseModel):
    browsing: str
    ordering: str
    design: str
    suggestions: str
    rating: Annotated[float, Field(strict=True, ge=0, le=10)]


class SurveyUpdateDto(BaseModel):
    browsing: str | None = None
    ordering: str | None = None
    design: str | None = None
    suggestions: str | None = None
    rating: Annotated[float, Field(strict=True, ge=0, le=10)] | None = None
