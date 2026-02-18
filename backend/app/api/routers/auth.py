from fastapi import APIRouter
from app.schemas.auth import (
    TokenResponse,
    RegisterRequest,
    LoginRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=TokenResponse)
def register(payload: RegisterRequest):
    return {
        "access_token": "not a real token",
        "token_type": "bearer",
    }


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    return {
        "access_token": "not a real token",
        "token_type": "bearer",
    }
