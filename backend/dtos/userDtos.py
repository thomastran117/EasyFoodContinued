from pydantic import BaseModel


class UpdateUserDto(BaseModel):
    username: str | None = None
    phone: str | None = None
    address: str | None = None
    profileUrl: str | None = None
    description: str | None = None
