from contextlib import asynccontextmanager
from pathlib import Path
from secrets import compare_digest
from shutil import copyfileobj
from typing import Annotated
from typing import Optional
from uuid import uuid4

import httpx
from fastapi import Depends, FastAPI, File, HTTPException, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.ai import OpenAIEmbeddingService
from app.config import Settings, get_settings
from app.db import get_db, init_db, make_engine, make_session_factory, ping_db
from app.models import Document
from app.processing import process_document
from app.retrieval import answer_question, retrieve_chunks, search_result_response


class ChatRequest(BaseModel):
    question: str


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


def document_response(document: Document) -> dict:
    return {
        "id": document.id,
        "filename": document.filename,
        "content_type": document.content_type,
        "size_bytes": document.size_bytes,
        "status": document.status.value,
        "created_at": document.created_at,
        "updated_at": document.updated_at,
    }


def create_app(settings: Optional[Settings] = None) -> FastAPI:
    settings = settings or get_settings()
    engine = make_engine(settings.database_url)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        init_db(engine)
        yield

    app = FastAPI(title="Knovara", lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.state.SessionLocal = make_session_factory(engine)
    app.state.ai_service = OpenAIEmbeddingService(settings)

    def db_session(request: Request):
        yield from get_db(request.app.state.SessionLocal)

    def require_knovara_auth(request: Request) -> None:
        if not settings.knovara_api_key:
            raise HTTPException(status_code=503, detail="Knovara API key is not configured")

        scheme, _, token = request.headers.get("Authorization", "").partition(" ")
        if scheme.lower() != "bearer" or not compare_digest(token, settings.knovara_api_key):
            raise HTTPException(
                status_code=401,
                detail="Invalid Knovara API token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    @app.get("/health")
    def health(session: Annotated[Session, Depends(db_session)]):
        try:
            ping_db(session)
        except SQLAlchemyError as exc:
            raise HTTPException(status_code=503, detail="database unavailable") from exc
        return {"status": "ok", "database": "ok"}

    @app.post("/api/documents", status_code=201)
    def upload_document(
        request: Request,
        session: Annotated[Session, Depends(db_session)],
        file: UploadFile = File(...),
    ):
        filename = Path(file.filename or "").name
        if Path(filename).suffix.lower() != ".pdf":
            raise HTTPException(status_code=400, detail="Only PDF files can be uploaded")

        storage_dir = Path(settings.document_storage_dir)
        storage_dir.mkdir(parents=True, exist_ok=True)
        storage_path = storage_dir / f"{uuid4().hex}.pdf"

        with storage_path.open("wb") as target:
            copyfileobj(file.file, target)

        if storage_path.read_bytes()[:5] != b"%PDF-":
            storage_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail="Only PDF files can be uploaded")

        document = Document(
            filename=filename,
            content_type=file.content_type or "application/pdf",
            storage_path=str(storage_path),
            size_bytes=storage_path.stat().st_size,
        )
        session.add(document)
        session.commit()
        session.refresh(document)
        process_document(session, document, request.app.state.ai_service)
        return document_response(document)

    @app.get("/api/documents")
    def list_documents(session: Annotated[Session, Depends(db_session)]):
        documents = session.scalars(select(Document).order_by(Document.created_at.desc())).all()
        return [document_response(document) for document in documents]

    @app.get("/api/documents/{document_id}")
    def get_document(document_id: int, session: Annotated[Session, Depends(db_session)]):
        document = session.get(Document, document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return document_response(document)

    @app.delete("/api/documents/{document_id}", status_code=204)
    def delete_document(document_id: int, session: Annotated[Session, Depends(db_session)]):
        document = session.get(Document, document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        storage_path = Path(document.storage_path)
        session.delete(document)
        session.commit()
        storage_path.unlink(missing_ok=True)
        return None

    @app.post("/api/chat")
    def chat(
        request: Request,
        chat_request: ChatRequest,
        session: Annotated[Session, Depends(db_session)],
    ):
        question = chat_request.question.strip()
        if not question:
            raise HTTPException(status_code=400, detail="Question is required")
        try:
            return answer_question(session, question, request.app.state.ai_service)
        except (ValueError, httpx.HTTPError) as exc:
            raise HTTPException(status_code=503, detail="AI service unavailable") from exc

    @app.post("/collections/{collection_id}/search")
    def search_collection(
        collection_id: str,
        request: Request,
        search_request: SearchRequest,
        session: Annotated[Session, Depends(db_session)],
    ):
        require_knovara_auth(request)
        query = search_request.query.strip()
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        if not 1 <= search_request.top_k <= 20:
            raise HTTPException(status_code=400, detail="top_k must be between 1 and 20")

        try:
            query_embedding = request.app.state.ai_service.embed([query])[0]
            chunks = retrieve_chunks(session, query_embedding, limit=search_request.top_k)
        except (ValueError, httpx.HTTPError) as exc:
            raise HTTPException(status_code=503, detail="AI service unavailable") from exc
        return {"results": [search_result_response(chunk) for chunk in chunks]}

    return app


app = create_app()
