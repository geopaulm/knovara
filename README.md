# Knovara

Knovara is a minimal FastAPI RAG MVP: upload a PDF, index its text, ask a question, and get an answer with source citations.

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
DATABASE_URL=postgresql+psycopg://knovara:knovara@db:5432/knovara
DOCUMENT_STORAGE_DIR=storage/documents
AI_API_KEY=your_api_key_here
KNOVARA_API_KEY=your_search_token_here
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

## Frontend

The Next.js frontend lives in `frontend/`.

```sh
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

For the full demo workflow, keep the backend running in another terminal:

```sh
docker compose up --build
```

Set `NEXT_PUBLIC_API_BASE_URL` when the API is not running at `http://localhost:8000`:

```sh
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 npm run dev
```

Frontend checks:

```sh
cd frontend
npm run typecheck
npm run build
```

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

Search a collection with the Knovara-compatible RAG endpoint:

```sh
curl -X POST http://localhost:8000/collections/main/search \
  -H "Authorization: Bearer $KNOVARA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"What does the document say about refunds?","top_k":5}'
```

Search responses include a `results` array. Result items are citation-friendly objects with document title, source, page number, and text.

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
