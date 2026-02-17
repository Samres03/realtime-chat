from typing import TYPE_CHECKING

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.conversation_members import ConversationMembers
    from app.models.message import Message


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user")
    conversation_members: Mapped[list["ConversationMembers"]] = relationship(
        "ConversationMembers", back_populates="user", cascade="all, delete-orphan"
    )
