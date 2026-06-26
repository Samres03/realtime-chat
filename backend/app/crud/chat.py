from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
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
    users = {"owner": user_id, "member": other_user_id}
    for role, user_id in users.items():
        create_conversation_member(db, user_id, role, conversation.id)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_conversation_by_id(db: Session, conversation_id: int) -> Conversation:
    statement = select(Conversation).where(Conversation.id == conversation_id)
    return db.scalar(statement)


def get_conversations(db: Session, user_id: int) -> list[Conversation]:
    statement = (
        select(Conversation)
        .join(ConversationMember)
        .where(ConversationMember.user_id == user_id)
        .options(
            joinedload(Conversation.conversation_members).joinedload(
                ConversationMember.user
            )
        )
    )
    return db.scalars(statement).unique().all()


def is_conversation_member(db: Session, user_id: int, conversation_id: int) -> bool:
    statement = select(ConversationMember).where(
        ConversationMember.user_id == user_id,
        ConversationMember.conversation_id == conversation_id,
    )
    return db.scalar(statement) is not None
