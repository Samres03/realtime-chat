from pydantic import BaseModel, EmailStr, Field


class BaseAuthRequest(BaseModel):
    email: EmailStr
    password: Field(min_length=8, max_length=128)


class RegisterRequest(BaseAuthRequest):
    name: Field(min_lenght=2, max_length=128)


class LoginRequest(BaseAuthRequest):
    pass


class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserPublic
