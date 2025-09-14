from pydantic import BaseModel


class FoodCreateDto(BaseModel):
    name: str
    description: str
    price: float
    foodUrl: str
    calories: int | None = None
    tags: str | None = None
    ingredients: str | None = None


class FoodUpdateDto(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    foodUrl: str | None = None
    calories: int | None = None
    tags: str | None = None
    ingredients: str | None = None


class FoodResponse(BaseModel):
    pass
