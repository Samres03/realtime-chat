from sqlalchemy.orm import Session
from app.crud.chat import create_conversation
from app.crud.user import get_user_by_id
from fastapi.exceptions import HTTPException
from app.schemas.chat import ConversationResponse


class ChatService:
    # TODO: hay que controlar conversaciones 1:1 duplicadas
    @staticmethod
    def create_conversation_service(
        db: Session, user_id: int, other_user_id: int
    ) -> ConversationResponse:
        if user_id == other_user_id:
            raise HTTPException(
                status_code=400, detail="You cannot create a conversation with yourself"
            )
        users = [user_id, other_user_id]
        for user in users:
            if not get_user_by_id(db, user):
                raise HTTPException(status_code=404, detail="User not found")
        conversation = create_conversation(db, user_id, other_user_id)
        return ConversationResponse.model_validate(conversation)
