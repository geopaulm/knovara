from pathlib import Path

from fastapi.testclient import TestClient
from sqlalchemy import select

from app.config import Settings
from app.main import create_app
from app.models import Document, DocumentStatus
from pdf_helpers import pdf_with_text


PDF_WITH_TEXT = pdf_with_text("Alpha handbook text.")


class FakeAIService:
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[float(index), 0.5] for index, _ in enumerate(texts)]


def test_document_upload_list_get_delete(tmp_path):
    app = create_app(
        Settings(
            database_url=f"sqlite:///{tmp_path / 'test.db'}",
            document_storage_dir=str(tmp_path / "documents"),
        )
    )
    app.state.ai_service = FakeAIService()

    with TestClient(app) as client:
        bad = client.post(
            "/api/documents",
            files={"file": ("notes.txt", b"not a pdf", "text/plain")},
        )
        assert bad.status_code == 400
        assert bad.json()["detail"] == "Only PDF files can be uploaded"

        uploaded = client.post(
            "/api/documents",
            files={"file": ("handbook.pdf", PDF_WITH_TEXT, "application/pdf")},
        )
        assert uploaded.status_code == 201
        document = uploaded.json()
        assert document["filename"] == "handbook.pdf"
        assert document["status"] == "Ready"
        assert document["size_bytes"] == len(PDF_WITH_TEXT)
        assert len(list((tmp_path / "documents").glob("*.pdf"))) == 1

        with app.state.SessionLocal() as session:
            saved = session.scalars(select(Document).where(Document.id == document["id"])).one()
            assert saved.status == DocumentStatus.READY
            assert saved.chunks[0].document.filename == "handbook.pdf"
            assert saved.chunks[0].page_number == 1
            assert saved.chunks[0].position == 0
            assert saved.chunks[0].text == "Alpha handbook text."
            assert saved.chunks[0].embedding.embedding == [0.0, 0.5]

        listed = client.get("/api/documents")
        assert listed.status_code == 200
        assert [item["id"] for item in listed.json()] == [document["id"]]

        fetched = client.get(f"/api/documents/{document['id']}")
        assert fetched.status_code == 200
        assert fetched.json()["status"] == "Ready"

        failed = client.post(
            "/api/documents",
            files={"file": ("empty.pdf", b"%PDF-1.7\n", "application/pdf")},
        )
        assert failed.status_code == 201
        failed_document = failed.json()
        assert failed_document["status"] == "Failed"

        deleted = client.delete(f"/api/documents/{document['id']}")
        assert deleted.status_code == 204

        deleted_failed = client.delete(f"/api/documents/{failed_document['id']}")
        assert deleted_failed.status_code == 204
        assert list(Path(tmp_path / "documents").glob("*.pdf")) == []

        missing = client.get(f"/api/documents/{document['id']}")
        assert missing.status_code == 404
