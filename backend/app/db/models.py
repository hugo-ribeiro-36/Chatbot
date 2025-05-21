from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from app.db.database import Base
from sqlalchemy.orm import relationship
from datetime import datetime

class Feedback(Base):
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String)
    version = Column(String)
    message = Column(Text)
    user_message = Column(Text)
    rating = Column(Integer)
    comment = Column(Text)

class Knowledge(Base):
    __tablename__ = "knowledge"
    id = Column(Integer, primary_key=True, index=True)
    keyword = Column(String, unique=True)
    content = Column(Text)

class PromptConfig(Base):
    __tablename__ = "prompt_config"
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String, unique=True)
    prompt = Column(Text)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True)
    version = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("Message", back_populates="conversation")
    file_id =Column(String)

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"))
    role = Column(String)  # 'user' or 'assistant'
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")