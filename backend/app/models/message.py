from typing import TYPE_CHECKING

from app.db.base import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.conversations import Conversation
    from app.models.users import User


class Message(Base, TimestampMixin):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    content: Mapped[str] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id"), nullable=False, index=True
    )
    user: Mapped["User"] = relationship("User", back_populates="messages")
    conversation: Mapped["Conversation"] = relationship(
        "Conversation", back_populates="messages"
    )
