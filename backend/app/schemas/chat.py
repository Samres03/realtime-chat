from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from app.schemas.user import UserPublic


class CreateConversationRequest(BaseModel):
    # escalable para mas de 2 usuarios (grupos)
    other_user_id: int = Field(gt=0)


class ConversationMemberPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    user: UserPublic
    role: str


class ConversationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    conversation_members: list[ConversationMemberPublic]
    created_at: datetime
