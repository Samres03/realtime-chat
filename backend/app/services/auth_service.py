from app.schemas.auth_scheme import TokenResponse
from app.schemas.user_scheme import UserPublic
from app.crud.user import create_user
from app.core.security import hash_password, validate_password, verify_password
from app.core.security import create_access_token
from app.crud.user import get_user_by_mail

from sqlalchemy.orm import Session

from fastapi.exceptions import HTTPException


class AuthService:
    @staticmethod
    def build_token_response(user_id: int, name: str, email: str) -> TokenResponse:
        access_token = create_access_token(user_id)
        return TokenResponse(
            access_token=access_token,
            user=UserPublic(
                id=user_id,
                name=name,
                email=email,
            ),
        )

    @staticmethod
    def create_user_service(
        db: Session, name: str, email: str, password: str
    ) -> TokenResponse:
        validate_password(password)
        password_hash = hash_password(password)
        user = create_user(db, name, email, password_hash)
        return AuthService.build_token_response(
            user_id=user.id,
            name=user.name,
            email=user.email,
        )

    @staticmethod
    def login_user_service(db: Session, email: str, password: str) -> TokenResponse:
        user = get_user_by_mail(db, email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid Mail")
        if not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid Password")

        return AuthService.build_token_response(
            user_id=user.id,
            name=user.name,
            email=user.email,
        )
