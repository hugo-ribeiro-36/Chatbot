
# 💬Chatbot

A conversational web chatbot built with FastAPI (backend) and React (frontend), integrated with OpenAI's GPT and a semantic knowledge base powered by ChromaDB.

Designed to support version-based A/B testing, user feedback collection, configurable prompt strategies, and deep integration of structured external knowledge.

---

## 🔧 Tech Stack

| Layer       | Technology                     |
|-------------|--------------------------------|
| Frontend    | React + TypeScript             |
| Backend     | FastAPI                        |
| LLM         | OpenAI (GPT-4o / GPT-3.5 Turbo)|
| Knowledge   | ChromaDB + OpenAI Embeddings   |
| Database    | SQLite (for feedback)          |
| Vector Store| chromadb                       |

---

## ✅ Core Features

| Feature                            | Status    |
|------------------------------------|-----------|
| GPT-powered chat engine            | ✅ Done    |
| Prompt versioning (A/B)            | ✅ Done    |
| Feedback on responses              | ✅ Done    |
| Feedback persistence               | ✅ Done    |
| CRUD for knowledge entries         | ✅ Done    |
| Dynamic prompt configuration       | ✅ Done    |
| Vector-based knowledge search      | ✅ Done    |
| Frontend UI                        | ✅ Done    |

---

## 📁 Project Structure

```
chatbot/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/     # API routes
│   │   ├── core/                 # Prompt config, chatbot engine, vector logic
│   │   ├── db/                   # SQLAlchemy models
│   │   ├── schemas/              # Pydantic models
│   │   └── main.py               # FastAPI app entrypoint
│   └── chromadb/                 # ChromaDB persistent store
└── frontend/
    └── src/                      # React components
```

---

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone
cd chatbot
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at http://localhost:8000

Visit http://localhost:8000/docs for Swagger UI.

☑️ Before running, ensure your OpenAI API key is configured:

Option A: Hardcoded in app/core/knowledge_vector.py  and app/core/chatbot_engine.py
Option B (recommended): use environment variable OPENAI_API_KEY or .env file

### 3. Frontend setup

```bash
cd frontend
npm install
npm start
```

Frontend runs at http://localhost:3000

---

## 🧠 Design Rationale

We made the following key design choices:

- ✨ GPT Integration: GPT-4o was used for better reasoning. To reduce hallucinations, we constrained the model using injected context when knowledge matched.

- 🔀 A/B Testing: Prompt versions are assigned per conversation and persisted for consistent feedback comparisons.

- 📚 Knowledge Search: Vector search (via ChromaDB) was chosen over static keywords to support semantically rich matching of uploaded text files.

- ⚙️ Dynamic Configuration: Prompt logic (version A/B) is editable via API to tune the assistant’s tone and behavior.

- 📊 Feedback Logging: Ratings + comments are stored per message, linked to both the version and the user’s original message, enabling longitudinal analysis.

---

## 🧪 Test It

Try asking:

- "What is AquaShield-X?" → (if your knowledge base includes zenthos.txt)
- "How long does shipping take?" → (tests fallback to prompt A/B)

Try uploading:

- A .txt file via POST /api/v1/knowledge-vector/upload
- A thumbs up/down rating and optional comment via the frontend

---

## 📘 To Do / Future Work

- [ ] Adaptive Learning
