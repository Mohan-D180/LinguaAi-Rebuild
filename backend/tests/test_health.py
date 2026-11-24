"""Tests for the public health endpoint."""

from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app


def test_health_returns_application_status_and_version() -> None:
    app = create_app(Settings(app_name="LinguaAi Test", api_version="v1"))

    with TestClient(app) as client:
        response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {
        "application_name": "LinguaAi Test",
        "status": "ok",
        "api_version": "v1",
    }


def test_api_documentation_is_available() -> None:
    with TestClient(create_app()) as client:
        response = client.get("/docs")

    assert response.status_code == 200
