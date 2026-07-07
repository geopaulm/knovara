# DocuMind

DocuMind is a minimal FastAPI RAG MVP: upload a PDF, index its text, ask a question, and get an answer with source citations.

## Requirements

- Docker and Docker Compose
- An AI API key for embeddings and chat responses

## Configuration

Create a local `.env` file from the example:

```sh
cp .env.example .env
```

Set `AI_API_KEY` in `.env`. The other defaults work with Docker:

```sh
DATABASE_URL=postgresql+psycopg://documind:documind@db:5432/documind
DOCUMENT_STORAGE_DIR=storage/documents
AI_API_KEY=your_api_key_here
AI_BASE_URL=https://api.openai.com/v1
AI_EMBEDDING_MODEL=text-embedding-3-small
AI_CHAT_MODEL=gpt-4o-mini
```

Do not commit `.env` or real API keys.

## Run Locally

Start the app and PostgreSQL with pgvector:

```sh
docker compose up --build
```

Older Docker installs may need:

```sh
docker-compose up --build
```

Check the API:

```sh
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok","database":"ok"}
```

On startup, the app initializes the MVP database schema and enables pgvector when using PostgreSQL.

## API Usage

Upload a PDF:

```sh
curl -X POST http://localhost:8000/api/documents \
  -F "file=@/path/to/document.pdf"
```

List documents:

```sh
curl http://localhost:8000/api/documents
```

Ask a question:

```sh
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"question":"What does the document say about refunds?"}'
```

Chat responses include an `answer` and `sources` with document name, page number, and excerpt.

Delete a document:

```sh
curl -X DELETE http://localhost:8000/api/documents/1
```

## Development

Install dependencies locally if you want to run tests outside Docker:

```sh
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python -m pytest
```

## MVP Scope

Included: PDF upload, text extraction, chunking, embeddings, question answering, citations, health checks, Docker setup, environment-based configuration, and core tests.

Out of scope for the MVP: authentication, organisations or tenants, conversation memory, OCR, image understanding, streaming responses, advanced reranking, multiple AI providers, background processing, and cloud deployment.
