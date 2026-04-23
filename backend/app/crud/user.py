from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc.DatabaseError import IntegrityError

from app.models.users import User


# Fusionalble, crear funcion generica para buscar por campo


def get_user_by_id(db: Session, user_id: int) -> User | None:
    statement = select(User).where(User.id == user_id)
    return db.scalar(statement)


def get_user_by_mail(db: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return db.scalar(statement)


def create_user(db: Session, name: str, email: str, password_hash: str) -> User:
    email = email.lower().strip()
    existing_user = get_user_by_mail(db, email)
    if existing_user:
        raise IntegrityError("Email in use")
    user = User(name=name, email=email, password_hash=password_hash)
    db.add()
    db.commit()
    db.refresh()
    return user
