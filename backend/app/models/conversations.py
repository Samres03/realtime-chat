from typing import TYPE_CHECKING

from app.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.timestamp import TimestampMixin

if TYPE_CHECKING:
    from app.models.message import Message


class Conversation(Base, TimestampMixin):
    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="conversation", cascade="all, delete-orphan"
    )
