from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from pdf_helpers import pdf_with_text


class FakeAIService:
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[1.0, 0.0] if "alpha" in text.lower() else [0.0, 1.0] for text in texts]

    def answer(self, prompt: str) -> str:
        assert "Alpha handbook text." in prompt
        assert "Not enough information in the uploaded documents." in prompt
        return "Alpha handbook text."


def test_chat_answers_from_retrieved_context(tmp_path):
    app = create_app(
        Settings(
            database_url=f"sqlite:///{tmp_path / 'test.db'}",
            document_storage_dir=str(tmp_path / "documents"),
        )
    )
    app.state.ai_service = FakeAIService()

    with TestClient(app) as client:
        client.post(
            "/api/documents",
            files={"file": ("handbook.pdf", pdf_with_text("Alpha handbook text."), "application/pdf")},
        )

        response = client.post("/api/chat", json={"question": "What does alpha say?"})

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Alpha handbook text.",
        "sources": [
            {
                "document_name": "handbook.pdf",
                "page_number": 1,
                "excerpt": "Alpha handbook text.",
            }
        ],
    }


def test_chat_falls_back_without_context(tmp_path):
    app = create_app(
        Settings(
            database_url=f"sqlite:///{tmp_path / 'test.db'}",
            document_storage_dir=str(tmp_path / "documents"),
        )
    )
    app.state.ai_service = FakeAIService()

    with TestClient(app) as client:
        response = client.post("/api/chat", json={"question": "Anything?"})

    assert response.status_code == 200
    assert response.json() == {
        "answer": "Not enough information in the uploaded documents.",
        "sources": [],
    }


def test_chat_reports_ai_service_errors(tmp_path):
    app = create_app(
        Settings(
            database_url=f"sqlite:///{tmp_path / 'test.db'}",
            document_storage_dir=str(tmp_path / "documents"),
        )
    )

    with TestClient(app) as client:
        response = client.post("/api/chat", json={"question": "Anything?"})

    assert response.status_code == 503
    assert response.json()["detail"] == "AI service unavailable"
