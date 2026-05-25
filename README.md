# 🏥 AI Medical Assistant

A production-grade **Medical AI Assistant API** built with FastAPI, featuring RAG (Retrieval-Augmented Generation) over medical documents, conversation history, and JWT authentication.

---

## 🚀 Features

- **RAG Pipeline** — Upload medical PDFs and ask questions about them with accurate, context-aware answers
- **Per-user Document Scoping** — Each user's documents are isolated; no cross-user data leakage
- **Conversation History** — Multi-turn conversations stored in PostgreSQL
- **JWT Authentication** — Secure access/refresh token system with bcrypt password hashing
- **Background Processing** — PDF parsing and embedding happens asynchronously after upload
- **Vector Search** — Semantic search over medical documents using Qdrant
- **Google Embeddings** — `gemini-embedding-001` for high-quality medical text embeddings
- **LLM Integration** — Ollama (local) or Google Gemini for response generation

---

## 🧱 Tech Stack

| Layer | Technology |
|---|---|
| **Framework** | FastAPI (async) |
| **Database** | PostgreSQL + SQLAlchemy 2.0 (async) |
| **Vector DB** | Qdrant |
| **Embeddings** | Google `gemini-embedding-001` |
| **LLM** | Ollama (`llama3.2:1b`) / Google Gemini |
| **PDF Parsing** | PyMuPDF (fitz) |
| **Auth** | JWT (PyJWT) + bcrypt |
| **Migrations** | Alembic |
| **Package Manager** | uv |
| **Containerization** | Docker Compose |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      FastAPI App                         │
├──────────────┬──────────────┬──────────────┬────────────┤
│  Auth Module │ User Module  │  Doc Module  │ Chat Module│
├──────────────┴──────────────┴──────────────┴────────────┤
│                      RAG Pipeline                        │
│         Embedder → Vector Store → Pipeline               │
├────────────────────┬────────────────────────────────────┤
│    PostgreSQL       │           Qdrant                   │
│  (users, docs,     │    (document vectors)               │
│   conversations,   │                                     │
│   messages)        │                                     │
└────────────────────┴────────────────────────────────────┘
```

---

## 📁 Project Structure

```
ai-medical-assistant/
├── app/
│   ├── core/
│   │   ├── config.py          # Pydantic settings from .env
│   │   ├── database.py        # SQLAlchemy async engine + session
│   │   ├── dependencies.py    # FastAPI dependencies (get_db, get_current_user)
│   │   ├── exceptions.py      # Centralized HTTP exceptions
│   │   └── security.py        # JWT + bcrypt
│   ├── modules/
│   │   ├── auth/              # Register, login, refresh
│   │   ├── user/              # User model, DTOs, service
│   │   ├── document/          # PDF upload, metadata
│   │   └── chat/              # Conversations, messages, ask
│   └── rag/
│       ├── embedder.py        # Google Gemini embeddings
│       ├── vector_store.py    # Qdrant client
│       └── pipeline.py        # Extract → Chunk → Embed → Store
├── alembic/                   # DB migrations
├── docker-compose.yaml
├── pyproject.toml
└── .env.example
```

---

## ⚙️ Setup & Installation

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Ollama](https://ollama.com/download) (for local LLM)

---

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/ai-medical-assistant.git
cd ai-medical-assistant
```

### 2. Install dependencies

```bash
uv sync
source .venv/bin/activate      # Linux/Mac
.venv\Scripts\activate         # Windows
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` with your values:

```env
APP_NAME=AI Medical Assistant
DEBUG=True

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/medical_ai

QDRANT_URL=http://localhost:6333
QDRANT_COLLECTION=medical_docs
VECTOR_SIZE=768

GOOGLE_API_KEY=your_google_api_key_here

OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b

JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_ACCESS_EXPIRE_MINUTES=60
JWT_REFRESH_EXPIRE_DAYS=7

UPLOAD_DIR=uploads
CHUNK_SIZE=800
CHUNK_OVERLAP=100
```


### 4. Start infrastructure

```bash
docker compose up -d postgres qdrant
```

### 5. Run database migrations

```bash
alembic upgrade head
```

### 6. Start Ollama and pull model

```bash
ollama pull llama3.2:1b
```

### 7. Run the server

```bash
fastapi dev app/main.py
```

API docs available at: `http://localhost:8000/docs`

---

## 📡 API Endpoints

### Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register a new user |
| POST | `/auth/login` | Login and get tokens |
| POST | `/auth/refresh` | Refresh access token |
| GET | `/auth/me` | Get current user |

### Documents
| Method | Endpoint | Description |
|---|---|---|
| POST | `/documents/upload` | Upload a PDF (async processing) |
| GET | `/documents` | List user's documents |
| GET | `/documents/{id}` | Get document details |
| DELETE | `/documents/{id}` | Delete a document |

### Chat
| Method | Endpoint | Description |
|---|---|---|
| POST | `/chat/conversations` | Create a new conversation |
| GET | `/chat/conversations` | List user's conversations |
| POST | `/chat/conversations/{id}/ask` | Ask a question |
| GET | `/chat/conversations/{id}/messages` | Get conversation history |

---

## 🔄 RAG Pipeline Flow

```
1. User uploads PDF
        ↓
2. File saved to disk + metadata saved to PostgreSQL (status: "processing")
        ↓
3. 202 Accepted returned immediately
        ↓
4. Background task starts:
   → Extract text from PDF (PyMuPDF)
   → Split into chunks (sentence-aware, 800 chars)
   → Embed each chunk (Google gemini-embedding-001, 768 dims)
   → Store vectors in Qdrant with user_id + document_id in payload
        ↓
5. Status updated to "ready" or "failed"

When user asks a question:
1. Embed the question (retrieval_query task type)
2. Search Qdrant (filtered by user_id)
3. Retrieve top 5 relevant chunks
4. Build prompt with context + conversation history
5. Send to Ollama/Gemini
6. Save messages to PostgreSQL
7. Return answer + sources
```

---


## 🗂️ Environment Variables

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | PostgreSQL connection string | required |
| `QDRANT_URL` | Qdrant server URL | `http://localhost:6333` |
| `QDRANT_COLLECTION` | Qdrant collection name | `medical_docs` |
| `VECTOR_SIZE` | Embedding dimension | `768` |
| `GOOGLE_API_KEY` | Google AI Studio API key | required |
| `OLLAMA_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model name | `llama3.2:1b` |
| `JWT_SECRET_KEY` | JWT signing secret | required |
| `JWT_ACCESS_EXPIRE_MINUTES` | Access token expiry | `60` |
| `JWT_REFRESH_EXPIRE_DAYS` | Refresh token expiry | `7` |
| `UPLOAD_DIR` | Directory for uploaded PDFs | `uploads` |
| `CHUNK_SIZE` | PDF chunk size in characters | `800` |
| `CHUNK_OVERLAP` | Chunk overlap in characters | `100` |

---

## 📝 License

MIT License — feel free to use this project as a reference or starting point.

---

## 👤 Author

**Ali Raza Khan**
- Software Engineer
- Stack: NestJS · FastAPI · Node.js · Python
- GitHub: [@AliYusufzai](https://github.com/AliYusufzai)