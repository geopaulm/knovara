from __future__ import annotations

from enum import Enum
from typing import Optional

from sqlalchemy import DateTime, Enum as SQLEnum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import UserDefinedType


class Base(DeclarativeBase):
    pass


class Vector(UserDefinedType):
    cache_ok = True

    def __init__(self, dimensions: int) -> None:
        self.dimensions = dimensions

    def get_col_spec(self, **kw) -> str:
        return f"VECTOR({self.dimensions})"

    def bind_processor(self, dialect):
        def process(value):
            if value is None or isinstance(value, str):
                return value
            return "[" + ",".join(str(number) for number in value) + "]"

        return process

    def result_processor(self, dialect, coltype):
        def process(value):
            if value is None or isinstance(value, list):
                return value
            return [float(number) for number in value.strip("[]").split(",") if number]

        return process


class DocumentStatus(str, Enum):
    UPLOADED = "Uploaded"
    PROCESSING = "Processing"
    READY = "Ready"
    FAILED = "Failed"


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    storage_path: Mapped[str] = mapped_column(String(500), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[DocumentStatus] = mapped_column(
        SQLEnum(
            DocumentStatus,
            values_callable=lambda status: [item.value for item in status],
            native_enum=False,
        ),
        default=DocumentStatus.UPLOADED,
        nullable=False,
    )
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[object] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    chunks: Mapped[list["DocumentChunk"]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True
    )
    page_number: Mapped[Optional[int]] = mapped_column(Integer)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    document: Mapped[Document] = relationship(back_populates="chunks")
    embedding: Mapped[Optional["ChunkEmbedding"]] = relationship(
        back_populates="chunk", cascade="all, delete-orphan", uselist=False
    )


class ChunkEmbedding(Base):
    __tablename__ = "chunk_embeddings"

    id: Mapped[int] = mapped_column(primary_key=True)
    chunk_id: Mapped[int] = mapped_column(
        ForeignKey("document_chunks.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    embedding: Mapped[list[float]] = mapped_column(Vector(1536), nullable=False)

    chunk: Mapped[DocumentChunk] = relationship(back_populates="embedding")
