# Knovara MVP Plan

This plan breaks the Knovara MVP into implementation milestones. Each milestone should leave the project in a working or verifiable state and build toward the success criteria in `requirements.txt`.

## Milestone 1: Project Foundation

### Goals

- Create the basic FastAPI application structure.
- Add local development configuration.
- Establish database connectivity.
- Provide a predictable way to run the app locally.

### Deliverables

- FastAPI app with a health check endpoint.
- SQLAlchemy database setup.
- PostgreSQL and pgvector configured through Docker.
- Environment-based configuration.
- `.env.example` with required variables.
- Initial README setup instructions.

### Completion Criteria

- The app starts locally with Docker.
- `GET /health` returns a successful response.
- The backend can connect to PostgreSQL.
- No secrets or API keys are committed.

## Milestone 2: Data Model and Persistence

### Goals

- Define the database schema needed for documents, chunks, and vector embeddings.
- Support lifecycle tracking for uploaded documents.

### Deliverables

- Document metadata model.
- Document chunk model.
- Embedding storage using pgvector.
- Document status field supporting:
  - `Uploaded`
  - `Processing`
  - `Ready`
  - `Failed`
- Database migrations or initialization workflow.
- Cascade deletion for chunks and embeddings when a document is deleted.

### Completion Criteria

- Documents can be created, queried, updated, and deleted in the database.
- Deleting a document removes its associated chunks and embeddings.
- Document processing status can be persisted and updated.

## Milestone 3: Document Upload and Management API

### Goals

- Allow users to upload, list, inspect, and delete PDF documents.
- Validate uploaded files before processing.

### Deliverables

- `POST /api/documents`
- `GET /api/documents`
- `GET /api/documents/{id}`
- `DELETE /api/documents/{id}`
- PDF-only upload validation.
- Local document storage.
- Basic upload and document management tests.

### Completion Criteria

- A PDF can be uploaded through the API.
- Non-PDF files are rejected with a useful error.
- Uploaded documents appear in the document list.
- Document details include processing status.
- Documents can be deleted through the API.

## Milestone 4: PDF Processing and Chunking

### Goals

- Extract text from uploaded PDFs.
- Split extracted content into retrievable chunks with useful metadata.

### Deliverables

- PDF text extraction service.
- Chunking service.
- Chunk metadata including:
  - Document ID
  - Document name
  - Page number, where available
  - Chunk position
- Processing status updates for success and failure cases.
- Tests for PDF extraction and chunking behavior.

### Completion Criteria

- Uploaded PDFs move through `Uploaded`, `Processing`, and `Ready` states.
- Failed processing sets the document status to `Failed`.
- Extracted text is split into chunks and stored in the database.
- Chunks retain enough metadata to support citations.

## Milestone 5: AI Service Layer and Embeddings

### Goals

- Add a replaceable AI provider integration.
- Generate and store embeddings for document chunks.

### Deliverables

- Dedicated AI service interface.
- Embedding generation implementation.
- Configuration for AI API credentials through environment variables.
- Embedding generation during document processing.
- Tests using mocked AI responses.

### Completion Criteria

- Each processed chunk has an embedding stored in pgvector.
- AI provider access is isolated behind a service layer.
- Tests do not require real API calls.

## Milestone 6: Retrieval and Question Answering

### Goals

- Let users ask natural-language questions about uploaded documents.
- Retrieve relevant chunks and generate answers grounded in those chunks.

### Deliverables

- `POST /api/chat`
- Question embedding generation.
- Vector similarity search against document chunks.
- Top matching chunk selection.
- Prompt construction that instructs the model to answer only from retrieved context.
- Clear fallback answer when context is insufficient.
- Tests for retrieval and answer generation flow.

### Completion Criteria

- A user can submit a question and receive an answer.
- Answers are generated from retrieved document context.
- The model is instructed not to invent unavailable information.
- Insufficient context produces a clear "not enough information" response.

## Milestone 7: Source Citations

### Goals

- Show users which document content was used to generate an answer.
- Include enough source detail to make answers auditable.

### Deliverables

- Source citation data returned from `POST /api/chat`.
- Citation fields:
  - Document name
  - Page number, where available
  - Relevant text excerpt
- API response shape suitable for expandable source display.
- Tests for citation response data.

### Completion Criteria

- Each answer includes the retrieved sources used to generate it.
- Sources include document names and excerpts.
- Page numbers are included when available.

## Milestone 8: MVP Hardening

### Goals

- Improve reliability, developer experience, and basic production hygiene for the local MVP.

### Deliverables

- Basic API error handling.
- Validation errors with useful messages.
- Core automated test suite.
- README with setup, environment, Docker, and API usage instructions.
- Final review against MVP scope and out-of-scope list.

### Completion Criteria

- Core tests pass locally.
- The app can be started from a clean checkout using documented steps.
- The README explains how to upload a PDF and ask a question.
- Out-of-scope features are not accidentally included.

## MVP Acceptance Checklist

- The application starts locally.
- A user can upload a PDF document.
- The document is processed and indexed.
- A user can ask a question about the document.
- The application returns a relevant answer based on retrieved content.
- The answer includes source citations.
- The app includes Docker-based local setup.
- API keys and secrets are kept out of source control.
- Core functionality is covered by automated tests.
