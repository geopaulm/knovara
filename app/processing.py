from __future__ import annotations

from pypdf import PdfReader
from sqlalchemy.orm import Session

from app.ai import AIService
from app.models import Document, DocumentChunk, DocumentStatus
from app.models import ChunkEmbedding


def extract_pdf_text(path: str) -> list[tuple[int | None, str]]:
    reader = PdfReader(path)
    pages = []
    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = " ".join(text.split())
        if text:
            pages.append((index, text))
    return pages


def chunk_pages(pages: list[tuple[int | None, str]], max_chars: int = 1000) -> list[DocumentChunk]:
    chunks = []
    for page_number, text in pages:
        words = text.split()
        current: list[str] = []
        for word in words:
            if current and len(" ".join([*current, word])) > max_chars:
                chunks.append(
                    DocumentChunk(page_number=page_number, position=len(chunks), text=" ".join(current))
                )
                current = []
            current.append(word)
        if current:
            chunks.append(DocumentChunk(page_number=page_number, position=len(chunks), text=" ".join(current)))
    return chunks


def process_document(session: Session, document: Document, ai_service: AIService) -> None:
    document.status = DocumentStatus.PROCESSING
    session.commit()

    try:
        chunks = chunk_pages(extract_pdf_text(document.storage_path))
        if not chunks:
            raise ValueError("no extractable text")
        embeddings = ai_service.embed([chunk.text for chunk in chunks])
        if len(embeddings) != len(chunks):
            raise ValueError("embedding count mismatch")
        for chunk, embedding in zip(chunks, embeddings):
            chunk.embedding = ChunkEmbedding(embedding=embedding)
        document.chunks = chunks
        document.status = DocumentStatus.READY
    except Exception:
        document.chunks = []
        document.status = DocumentStatus.FAILED
    session.commit()
    session.refresh(document)
