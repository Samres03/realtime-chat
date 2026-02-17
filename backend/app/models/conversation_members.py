from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, func, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.conversations import Conversation
    from app.models.users import User


class ConversationMember(Base):
    __tablename__ = "conversation_members"

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        String(20),
        server_default="member",
        nullable=False,
    )

    conversation: Mapped["Conversation"] = relationship(
        back_populates="conversation_members"
    )
    user: Mapped["User"] = relationship(back_populates="conversation_members")
