from fastapi import APIRouter, Depends
from app.services.auth_service import AuthService
from app.schemas.auth_scheme import (
    TokenResponse,
    RegisterRequest,
    LoginRequest,
)
from app.db.deps import get_db
from sqlalchemy.orm import Session
from app.api.deps import get_current_user
from app.schemas.user_scheme import UserPublic
from app.models.users import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=TokenResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    return AuthService.create_user_service(
        db, payload.name, payload.email, payload.password
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    return AuthService.login_user_service(db, payload.email, payload.password)


@router.get("/me", response_model=UserPublic)
def me(user: User = Depends(get_current_user)):
    return user
