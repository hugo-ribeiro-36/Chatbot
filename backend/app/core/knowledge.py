from app.db.database import db_session
from app.db.models import Knowledge
from app.schemas.knowledge import KnowledgeBase, KnowledgeUpdate

def search_knowledge(user_msg: str) -> str | None:
    entries = db_session.query(Knowledge).all()
    for entry in entries:
        if entry.keyword.lower() in user_msg.lower():
            return entry.content
    return None