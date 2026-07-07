from __future__ import annotations

import math

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai import AIService
from app.models import ChunkEmbedding, Document, DocumentChunk, DocumentStatus

FALLBACK_ANSWER = "Not enough information in the uploaded documents."


def cosine_similarity(left: list[float], right: list[float]) -> float:
    numerator = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def retrieve_chunks(session: Session, question_embedding: list[float], limit: int = 5) -> list[DocumentChunk]:
    chunks = session.scalars(
        select(DocumentChunk)
        .join(Document)
        .join(ChunkEmbedding)
        .where(Document.status == DocumentStatus.READY)
    ).all()
    ranked = sorted(
        chunks,
        key=lambda chunk: cosine_similarity(question_embedding, chunk.embedding.embedding),
        reverse=True,
    )
    return ranked[:limit]


def build_prompt(question: str, chunks: list[DocumentChunk]) -> str:
    context = "\n\n".join(
        f"Document: {chunk.document.filename}\nPage: {chunk.page_number or 'unknown'}\n{chunk.text}"
        for chunk in chunks
    )
    return (
        "Use only this context to answer the question. "
        f"If the answer is not present, reply exactly: {FALLBACK_ANSWER}\n\n"
        f"Context:\n{context}\n\nQuestion: {question}"
    )


def source_response(chunk: DocumentChunk) -> dict:
    return {
        "document_name": chunk.document.filename,
        "page_number": chunk.page_number,
        "excerpt": chunk.text,
    }


def answer_question(session: Session, question: str, ai_service: AIService) -> dict:
    question_embedding = ai_service.embed([question])[0]
    chunks = retrieve_chunks(session, question_embedding)
    if not chunks:
        return {"answer": FALLBACK_ANSWER, "sources": []}
    return {
        "answer": ai_service.answer(build_prompt(question, chunks)),
        "sources": [source_response(chunk) for chunk in chunks],
    }
