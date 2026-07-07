from pathlib import Path

from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_document_upload_list_get_delete(tmp_path):
    app = create_app(
        Settings(
            database_url=f"sqlite:///{tmp_path / 'test.db'}",
            document_storage_dir=str(tmp_path / "documents"),
        )
    )

    with TestClient(app) as client:
        bad = client.post(
            "/api/documents",
            files={"file": ("notes.txt", b"not a pdf", "text/plain")},
        )
        assert bad.status_code == 400
        assert bad.json()["detail"] == "Only PDF files can be uploaded"

        uploaded = client.post(
            "/api/documents",
            files={"file": ("handbook.pdf", b"%PDF-1.7\n", "application/pdf")},
        )
        assert uploaded.status_code == 201
        document = uploaded.json()
        assert document["filename"] == "handbook.pdf"
        assert document["status"] == "Uploaded"
        assert document["size_bytes"] == 9
        assert len(list((tmp_path / "documents").glob("*.pdf"))) == 1

        listed = client.get("/api/documents")
        assert listed.status_code == 200
        assert [item["id"] for item in listed.json()] == [document["id"]]

        fetched = client.get(f"/api/documents/{document['id']}")
        assert fetched.status_code == 200
        assert fetched.json()["status"] == "Uploaded"

        deleted = client.delete(f"/api/documents/{document['id']}")
        assert deleted.status_code == 204
        assert list(Path(tmp_path / "documents").glob("*.pdf")) == []

        missing = client.get(f"/api/documents/{document['id']}")
        assert missing.status_code == 404
