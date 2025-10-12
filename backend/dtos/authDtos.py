from pydantic import BaseModel, EmailStr


class LoginRequestDto(BaseModel):
    email: EmailStr
    password: str
    remember: bool


class SignupRequestDto(BaseModel):
    email: EmailStr
    password: str


class AuthResponseDto(BaseModel):
    token: str
    email: EmailStr
    id: int


class ForgotPasswordDto(BaseModel):
    email: EmailStr


class ChangePasswordDto(BaseModel):
    password: str


class MicrosoftAuthRequest(BaseModel):
    id_token: str


class GoogleAuthRequest(BaseModel):
    id_token: str
