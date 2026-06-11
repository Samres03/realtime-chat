from fastapi import APIRouter, Depends
from app.schemas.chat_scheme import CreateConversationRequest, ConversationResponse
from app.api.deps import get_current_user
from app.models.users import User
from app.db.deps import get_db
from sqlalchemy.orm import Session
from app.services.chat_service import ChatService


router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    payload: CreateConversationRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ChatService.create_conversation_service(db, user.id, payload.other_user_id)


@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation(
    conversation_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ChatService.get_conversation_by_id_service(db, conversation_id)
