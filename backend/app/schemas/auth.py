from pydantic import BaseModel, EmailStr, Field
from app.schemas.user import UserPublic


class BaseAuthRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RegisterRequest(BaseAuthRequest):
    name: str = Field(min_length=2, max_length=128)


class LoginRequest(BaseAuthRequest):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
