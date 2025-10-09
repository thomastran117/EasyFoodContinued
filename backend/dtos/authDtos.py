from pydantic import BaseModel, EmailStr


class AuthRequestDto(BaseModel):
    email: EmailStr
    password: str


class AuthResponseDto(BaseModel):
    token: str
    email: EmailStr
    id: int


class MicrosoftAuthRequest(BaseModel):
    id_token: str


class GoogleAuthRequest(BaseModel):
    id_token: str
