from pydantic import BaseModel

class KnowledgeBase(BaseModel):
    keyword: str
    content: str

class KnowledgeUpdate(BaseModel):
    content: str