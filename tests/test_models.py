from sqlalchemy import func, select

from app.db import init_db, make_engine, make_session_factory
from app.models import ChunkEmbedding, Document, DocumentChunk, DocumentStatus


def test_document_persistence_status_and_cascade_delete():
    engine = make_engine("sqlite:///:memory:")
    init_db(engine)
    SessionLocal = make_session_factory(engine)

    with SessionLocal() as session:
        document = Document(
            filename="handbook.pdf",
            content_type="application/pdf",
            storage_path="/tmp/handbook.pdf",
            size_bytes=123,
            chunks=[
                DocumentChunk(
                    page_number=1,
                    position=0,
                    text="hello",
                    embedding=ChunkEmbedding(embedding=[0.1, 0.2, 0.3]),
                )
            ],
        )
        session.add(document)
        session.commit()

        saved = session.scalars(select(Document).where(Document.filename == "handbook.pdf")).one()
        assert saved.status == DocumentStatus.UPLOADED
        assert saved.chunks[0].embedding.embedding == [0.1, 0.2, 0.3]

        saved.status = DocumentStatus.READY
        session.commit()
        assert session.get(Document, saved.id).status == DocumentStatus.READY

        session.delete(saved)
        session.commit()

        assert session.scalar(select(func.count()).select_from(Document)) == 0
        assert session.scalar(select(func.count()).select_from(DocumentChunk)) == 0
        assert session.scalar(select(func.count()).select_from(ChunkEmbedding)) == 0
