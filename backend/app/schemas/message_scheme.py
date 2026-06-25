from pydantic import BaseModel, ConfigDict, Field
from app.schemas.user_scheme import UserPublic
from datetime import datetime


class MessageRequest(BaseModel):
    content: str = Field(min_length=1, max_length=5000)
    conversation_id: int


class MessageResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content: str
    conversation_id: int
    user: UserPublic
    created_at: datetime
