from pydantic import BaseModel, EmailStr


class AuthRequestDto(BaseModel):
    email: EmailStr
    password: str


class AuthResponseDto(BaseModel):
    token: str
    email: EmailStr
    id: int
