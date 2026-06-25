from sqlalchemy.orm import Session
from app.schemas.message_scheme import MessageResponse
from app.crud.message import create_message, get_messages
from app.crud.chat import get_conversation_by_id, is_conversation_member
from fastapi.exceptions import HTTPException


class MessageService:
    @staticmethod
    def create_message_service(
        db: Session, message_content: str, user_id: int, conversation_id: int
    ) -> MessageResponse:
        if not get_conversation_by_id(db, conversation_id):
            raise HTTPException(status_code=404, detail="Conversation not found")
        if not is_conversation_member(db, user_id, conversation_id):
            raise HTTPException(
                status_code=403, detail="You are not a member of this conversation"
            )
        message = create_message(db, message_content, user_id, conversation_id)
        return MessageResponse.model_validate(message)

    @staticmethod
    def get_messages_service(
        db: Session,
        conversation_id: int,
        user_id: int,
        limit: int = 50,
        before_id: int | None = None,
    ) -> list[MessageResponse]:
        if not get_conversation_by_id(db, conversation_id):
            raise HTTPException(status_code=404, detail="Conversation not found")
        if not is_conversation_member(db, user_id, conversation_id):
            raise HTTPException(
                status_code=403, detail="You are not a member of this conversation"
            )
        messages = get_messages(db, conversation_id, limit, before_id)
        return [MessageResponse.model_validate(message) for message in messages]
