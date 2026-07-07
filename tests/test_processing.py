import logging

from app.db import init_db, make_engine, make_session_factory
from app.models import Document
from app.processing import chunk_pages, extract_pdf_text
from app.processing import process_document
from pdf_helpers import pdf_with_text


def test_extract_pdf_text_and_chunk_pages(tmp_path):
    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(pdf_with_text("First page.", "Second page here."))

    pages = extract_pdf_text(str(pdf))
    chunks = chunk_pages(pages, max_chars=12)

    assert pages == [(1, "First page."), (2, "Second page here.")]
    assert [(chunk.page_number, chunk.position, chunk.text) for chunk in chunks] == [
        (1, 0, "First page."),
        (2, 1, "Second page"),
        (2, 2, "here."),
    ]


class FailingAIService:
    def embed(self, texts: list[str]) -> list[list[float]]:
        raise RuntimeError("embedding exploded")


def test_process_document_logs_failures(tmp_path, caplog):
    pdf = tmp_path / "sample.pdf"
    pdf.write_bytes(pdf_with_text("Text that reaches embeddings."))
    engine = make_engine(f"sqlite:///{tmp_path / 'test.db'}")
    init_db(engine)

    with make_session_factory(engine)() as session:
        document = Document(
            filename="sample.pdf",
            content_type="application/pdf",
            storage_path=str(pdf),
            size_bytes=pdf.stat().st_size,
        )
        session.add(document)
        session.commit()
        session.refresh(document)

        with caplog.at_level(logging.ERROR, logger="app.processing"):
            process_document(session, document, FailingAIService())

    assert "Document processing failed for document_id=1 filename=sample.pdf" in caplog.text
    assert "embedding exploded" in caplog.text
