from sqlalchemy.orm import Session, joinedload
from app.models.message import Message
from sqlalchemy import select


def create_message(
    db: Session, message_content: str, user_id: int, conversation_id: int
) -> Message:
    message = Message(
        content=message_content, user_id=user_id, conversation_id=conversation_id
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    statement = (
        select(Message)
        .where(Message.id == message.id)
        .options(joinedload(Message.user))
    )
    return db.scalar(statement)


# SE IMPLEMENTA PAGINACION POR CURSOR-BASED, NO NECESARIO AFTER_ID POR EL USO DE WEBSOCKET
def get_messages(
    db: Session,
    conversation_id: int,
    limit: int = 50,
    before_id: int | None = None,
) -> list[Message]:
    messages = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .options(joinedload(Message.user))
    )
    if before_id:
        messages = messages.where(Message.id < before_id).order_by(Message.id.desc())
    else:
        messages = messages.order_by(Message.id.desc())
    rows = db.scalars(messages.limit(limit)).all()
    return list(reversed(rows))
