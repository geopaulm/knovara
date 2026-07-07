from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_health_checks_database():
    app = create_app(Settings(database_url="sqlite:///:memory:"))

    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


def test_frontend_origin_can_call_api():
    app = create_app(Settings(database_url="sqlite:///:memory:"))

    response = TestClient(app).options(
        "/api/documents",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:3000"
