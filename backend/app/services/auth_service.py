from app.schemas.auth import TokenResponse, UserPublic
from app.crud.user import create_user
from app.core.security import hash_password, validate_password

from sqlalchemy.orm import Session


class AuthService:
    @staticmethod
    def build_token_response(user_id: int, name: str, email: str) -> TokenResponse:
        return TokenResponse(
            access_token="not-a-real-token",
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
        create_user(db, name, email, password_hash)
