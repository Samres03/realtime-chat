from pydantic import BaseModel, Field
from datetime import datetime


class CreateConversationRequest(BaseModel):
    # escalable para mas de 2 usuarios (grupos)
    other_user_id: int = Field(gt=0)


class ConversationMemberPublic(BaseModel):
    id: int
    name: str
    email: str
    role: str


class ConversationResponse(BaseModel):
    id: int
    members: list[ConversationMemberPublic]
    created_at: datetime
