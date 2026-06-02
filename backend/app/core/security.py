import re
import jwt

from passlib.context import CryptContext

from app.core.errors import PasswordValidationException
from app.core.config import settings
from datetime import datetime, timezone, timedelta
from fastapi.exceptions import HTTPException


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def create_access_token(user_id: int) -> str:
    time_expires = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    payload = {
        "sub": str(user_id),
        "exp": time_expires,
    }
    return jwt.encode(
        payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token ha expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def validate_password(password: str):
    if len(password) < 8:
        raise PasswordValidationException(
            400, "La contraseña debe tener al menos 8 caracteres"
        )

    if not re.search(r"[A-Z]", password):
        raise PasswordValidationException(400, "Debe contener una mayúscula")

    if not re.search(r"[0-9]", password):
        raise PasswordValidationException(400, "Debe contener un número")
