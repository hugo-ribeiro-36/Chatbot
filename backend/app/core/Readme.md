# 🧠 Chatbot Application (FastAPI + React)

This is a full-stack AI chatbot system that integrates OpenAI’s powerful models with local knowledge search and file-based retrieval. It features real-time streaming responses, version-based A/B testing, vector-based memory, web search, and user feedback collection.

---

## 📁 Project Structure

```
chatbot/
├── backend/
│   ├── app/
│   │   ├── core/                 # Core logic: embedding search, prompts, LLM engine
│   │   ├── db/                   # Database models and session
│   │   ├── routes/               # FastAPI routes (chat, upload, feedback, etc.)
│   │   ├── schemas/              # Pydantic schemas for request/response validation
│   │   └── main.py               # FastAPI app entry point
│   ├── tests/                    # Unit tests for API endpoints
│   ├── requirements.txt
│   └── .env                      # API keys and environment variables (not committed)
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/           # Chat UI, feedback, file upload
│   │   ├── pages/                # Main chat interface
│   │   ├── utils/                # SSE streaming handler
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
```

---

## 💡 Features

- 🔄 **Streaming responses** with Server-Sent Events (SSE)
- 🧠 **Vector-based search** using ChromaDB and OpenAI embeddings
- 📄 **File upload** support with OpenAI Assistants API (retrieval tool)
- 🌍 **Web search** via GPT with web tool access
- 🧪 **A/B testing** of different system prompts
- 📊 **Feedback collection**: thumbs up/down + optional comment
- 💬 **Conversation history and switcher** to continue old chats

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/chatbot.git
cd chatbot
```

---

### 2. Backend Setup (FastAPI)

#### ✅ Environment Variables

Create a `.env` file inside `backend/` with the following:

```env
OPENAI_API_KEY=sk-...
CHROMA_PATH=./chromadb
DATABASE_URL=sqlite:///./chatbot.db
```

#### 🛠 Install and Run

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\\Scripts\\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Backend runs at: [http://localhost:8000](http://localhost:8000)

---

### 3. Frontend Setup (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at: [http://localhost:5173](http://localhost:5173)

---

## 🧪 Running Tests

From the backend root:

```bash
python -m unittest discover tests
```

---

## 🧱 Architectural Highlights

- **FastAPI** serves as a lightweight backend for handling chat, file uploads, feedback, and versioned prompt logic.
- **React** provides a responsive chat interface with real-time streaming and feedback controls.
- **ChromaDB** powers the vector store for semantic search on custom knowledge documents.
- **OpenAI Assistants API** allows file-based retrieval and long-context Q&A.
- **A/B Testing** logic assigns system prompts randomly per conversation and tracks performance.

---

## 🔐 API Keys & Security

Be sure to keep your `.env` file safe. Never commit it to version control. If deploying, use secrets management.

---

## 🧩 Next Steps

- Add authentication (optional)
- Store feedback analytics in a dashboard
- Deploy with Docker or cloud

---

## 🛠 Built With

- FastAPI
- React + Vite
- ChromaDB
- OpenAI API (GPT-4, GPT-3.5)
- SQLite

---

## 📬 Feedback

Pull requests and issues are welcome!
