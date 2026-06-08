from fastapi import APIRouter, Depends
from app.schemas.chat import CreateConversationRequest, ConversationResponse
from app.api.deps import get_current_user
from app.models.users import User
from app.db.deps import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    payload: CreateConversationRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return True
