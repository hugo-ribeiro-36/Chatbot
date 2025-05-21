from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.endpoints import feedback, analytics, knowledge, knowledge_vector, config, config_db, chatbot_stream, conversations
from app.db.database import create_tables

app = FastAPI(title="Chatbot")

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(feedback.router, prefix="/api/v1/feedback")
app.include_router(analytics.router, prefix="/api/v1/analytics")
app.include_router(knowledge.router, prefix="/api/v1/knowledge")
app.include_router(knowledge_vector.router,prefix="/api/v1/knowledge-vector",tags=["KnowledgeVector"])
app.include_router(config.router, prefix="/api/v1/config", tags=["Config"])
app.include_router(config_db.router, prefix="/api/v1/config-db", tags=["ConfigDB"])
app.include_router(chatbot_stream.router, prefix="/api/v1", tags=["ChatbotStream"])
app.include_router(conversations.router, prefix="/api/v1")

@app.on_event("startup")
async def startup():
    create_tables()
