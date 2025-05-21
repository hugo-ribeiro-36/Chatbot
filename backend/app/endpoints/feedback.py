from fastapi import APIRouter
from pydantic import BaseModel

from app.db.database import db_session
from app.db.models import Feedback

router = APIRouter()

class FeedbackIn(BaseModel):
    conversation_id: str
    version: str
    message: str
    user_message: str
    rating: int
    comment: str = ""

@router.post("/")
def submit_feedback(feedback: FeedbackIn):
    """
    Submits or updates feedback for a specific assistant message in a conversation.

    If feedback for the same message already exists, it will be updated with the new rating and comment.
    Otherwise, a new feedback entry is created.

    Args:
        feedback (FeedbackIn): Feedback input including conversation ID, version, message, rating, and optional comment.

    Returns:
        dict: A status message indicating success (e.g., {"status": "ok"}).
    """
    existing = db_session.query(Feedback).filter_by(
        conversation_id=feedback.conversation_id,
        message=feedback.message
    ).first()

    if existing:
        existing.rating = feedback.rating
        existing.comment = feedback.comment
    else:
        fb = Feedback(**feedback.dict())
        db_session.add(fb)

    db_session.commit()
    return {"status": "ok"}
