import re

from passlib import CryptContext

from app.core.errors import PasswordValidationException


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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
