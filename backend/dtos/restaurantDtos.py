from pydantic import BaseModel


class RestaurantCreateDto(BaseModel):
    name: str
    description: str
    location: str
    logoUrl: str


class RestaurantUpdateDto(BaseModel):
    name: str | None = None
    description: str | None = None
    location: str | None = None
    logoUrl: str | None = None
