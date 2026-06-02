from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService
from app.schemas.auth import (
    TokenResponse,
    RegisterRequest,
    LoginRequest,
)
from app.db.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService.create_user_service(
        db, payload.name, payload.email, payload.password
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login_user_service(db, payload.email, payload.password)
