from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from uuid import uuid4
from app.db.models import Conversation
from app.db.database import get_db

router = APIRouter()


@router.post("/conversations")
def create_conversation(db: Session = Depends(get_db)):
    """
    Creates a new conversation and returns its unique identifier.

    Returns:
        dict: A dictionary containing the new conversation ID (e.g., {"id": "uuid"}).
    """
    convo = Conversation(id=str(uuid4()))
    db.add(convo)
    db.commit()
    return {"id": convo.id}

@router.get("/conversations")
def list_conversations(db: Session = Depends(get_db)):
    """
    Retrieves all existing conversations ordered by creation time (most recent first).

    Returns:
        list[Conversation]: A list of all conversation records from the database.
    """
    return db.query(Conversation).order_by(Conversation.started_at.desc()).all()

@router.get("/conversations/{conversation_id}/messages")
def get_conversation_messages(conversation_id: str, db: Session = Depends(get_db)):
    """
    Retrieves all messages for a specific conversation.

    Args:
        conversation_id (str): The unique ID of the conversation.

    Returns:
        list[dict]: A list of message objects, each with role, content, and timestamp.

    Raises:
        HTTPException: If the conversation does not exist.
    """
    convo = db.query(Conversation).filter_by(id=conversation_id).first()
    if not convo:
        raise HTTPException(status_code=404, detail="Conversation not found")

    return [
        {"role": msg.role, "content": msg.content, "timestamp": msg.timestamp}
        for msg in convo.messages
    ]
