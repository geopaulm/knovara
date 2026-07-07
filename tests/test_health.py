from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def test_health_checks_database():
    app = create_app(Settings(database_url="sqlite:///:memory:"))

    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}
