from sqlalchemy.orm import Session
from app.crud.chat import create_conversation
from app.crud.user import get_user_by_id
from fastapi.exceptions import HTTPException
from app.schemas.chat_scheme import ConversationResponse
from app.crud.chat import get_conversation_by_id, get_conversations


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

    @staticmethod
    def get_conversation_by_id_service(
        db: Session, conversation_id: int
    ) -> ConversationResponse:
        conversation = get_conversation_by_id(db, conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        return ConversationResponse.model_validate(conversation)

    @staticmethod
    def get_conversations_service(
        db: Session, user_id: int
    ) -> list[ConversationResponse]:
        conversations = get_conversations(db, user_id)
        return [
            ConversationResponse.model_validate(conversation)
            for conversation in conversations
        ]
