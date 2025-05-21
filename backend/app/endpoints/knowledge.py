from fastapi import APIRouter
from app.db.database import db_session
from app.db.models import Knowledge
from app.schemas.knowledge import KnowledgeBase, KnowledgeUpdate

router = APIRouter()

@router.post("/")
def create_entry(entry: KnowledgeBase):
    existing = db_session.query(Knowledge).filter_by(keyword=entry.keyword).first()
    if existing:
        raise HTTPException(status_code=400, detail="Keyword already exists")
    new_entry = Knowledge(keyword=entry.keyword, content=entry.content)
    db_session.add(new_entry)
    db_session.commit()
    return {"status": "created"}

@router.get("/")
def list_entries():
    return db_session.query(Knowledge).all()

@router.put("/{keyword}")
def update_entry(keyword: str, update: KnowledgeUpdate):
    entry = db_session.query(Knowledge).filter_by(keyword=keyword).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    entry.content = update.content
    db_session.commit()
    return {"status": "updated"}

@router.delete("/{keyword}")
def delete_entry(keyword: str):
    entry = db_session.query(Knowledge).filter_by(keyword=keyword).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Not found")
    db_session.delete(entry)
    db_session.commit()
    return {"status": "deleted"}
