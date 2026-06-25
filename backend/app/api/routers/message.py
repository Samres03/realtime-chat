from fastapi import APIRouter, Depends
from app.schemas.message_scheme import MessageRequest, MessageResponse
from app.api.deps import get_current_user
from app.models.users import User
from app.db.deps import get_db
from sqlalchemy.orm import Session
from app.services.message_service import MessageService

router = APIRouter(prefix="/messages", tags=["messages"])


@router.post("/", response_model=MessageResponse)
def create_message(
    payload: MessageRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return MessageService.create_message_service(
        db, payload.content, user.id, payload.conversation_id
    )


@router.get("/{conversation_id}", response_model=list[MessageResponse])
def get_messages(
    conversation_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 50,
    before_id: int | None = None,
):
    return MessageService.get_messages_service(
        db, conversation_id, user.id, limit, before_id
    )


# TODO: EXPONER ENDPOINT PARA RECUPERAR EL SIGUIENTE BEFORE_ID Y ENDPOINT
# PARA SABER SI QUEDAN MENSAJES
