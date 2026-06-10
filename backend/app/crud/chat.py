from sqlalchemy.orm import Session
from app.models.conversations import Conversation
from app.models.conversation_members import ConversationMember


def create_conversation_member(
    db: Session, user_id: int, role: str, conversation_id: int
) -> ConversationMember:
    conversation_member = ConversationMember(
        user_id=user_id, role=role, conversation_id=conversation_id
    )
    db.add(conversation_member)
    return conversation_member


def create_conversation(db: Session, user_id: int, other_user_id: int) -> Conversation:
    conversation = Conversation()
    db.add(conversation)
    db.flush()
    # TODO: esto se debe hacer en un bucle para poder agregar mas de 2 usuarios
    create_conversation_member(db, user_id, "owner", conversation.id)
    create_conversation_member(db, other_user_id, "member", conversation.id)
    db.commit()
    db.refresh(conversation)
    return conversation
