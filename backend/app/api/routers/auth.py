from fastapi import APIRouter

from app.services.auth_service import AuthService
from app.schemas.auth import (
    TokenResponse,
    RegisterRequest,
    LoginRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=TokenResponse)
def register(payload: RegisterRequest):
    return AuthService.build_token_response(
        user_id=1,
        name=payload.name,
        email=payload.email,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    return AuthService.build_token_response(
        user_id=1,
        name="pending-user-name",
        email=payload.email,
    )
