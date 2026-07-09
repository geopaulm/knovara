from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app
from pdf_helpers import pdf_with_text


class FakeAIService:
    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = []
        for text in texts:
            lowered = text.lower()
            embeddings.append([1.0, 0.0] if "alpha" in lowered else [0.0, 1.0])
        return embeddings

    def answer(self, prompt: str) -> str:
        return "unused"


def make_app(tmp_path):
    app = create_app(
        Settings(
            database_url=f"sqlite:///{tmp_path / 'test.db'}",
            document_storage_dir=str(tmp_path / "documents"),
            knovara_api_key="test-token",
        )
    )
    app.state.ai_service = FakeAIService()
    return app


def test_knovara_search_returns_results(tmp_path):
    app = make_app(tmp_path)

    with TestClient(app) as client:
        client.post(
            "/api/documents",
            files={
                "file": (
                    "handbook.pdf",
                    pdf_with_text("Alpha handbook text.", "Beta policy text."),
                    "application/pdf",
                )
            },
        )

        response = client.post(
            "/collections/main/search",
            headers={"Authorization": "Bearer test-token"},
            json={"query": "alpha", "top_k": 1},
        )

    assert response.status_code == 200
    assert response.json() == {
        "results": [
            {
                "id": "chunk-1",
                "title": "handbook.pdf",
                "source": "handbook.pdf",
                "page_number": 1,
                "text": "Alpha handbook text.",
            }
        ]
    }


def test_knovara_search_requires_bearer_token(tmp_path):
    app = make_app(tmp_path)

    response = TestClient(app).post(
        "/collections/main/search",
        json={"query": "alpha", "top_k": 1},
    )

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_knovara_search_validates_query_and_top_k(tmp_path):
    app = make_app(tmp_path)
    client = TestClient(app)
    headers = {"Authorization": "Bearer test-token"}

    empty_query = client.post(
        "/collections/main/search",
        headers=headers,
        json={"query": " ", "top_k": 1},
    )
    bad_top_k = client.post(
        "/collections/main/search",
        headers=headers,
        json={"query": "alpha", "top_k": 0},
    )

    assert empty_query.status_code == 400
    assert empty_query.json()["detail"] == "Query is required"
    assert bad_top_k.status_code == 400
    assert bad_top_k.json()["detail"] == "top_k must be between 1 and 20"
