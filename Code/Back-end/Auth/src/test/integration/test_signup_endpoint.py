"""Integration tests for the user signup endpoint."""
from datetime import date
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
import pytest

from core.enum.Eresponse_auth import EResponseAuth
from core.database.session_manager import SessionManager
from main import app
from service.signup.service import SignupService


@pytest.fixture
def client():
    """Create a FastAPI test client with mocked database session dependency."""
    app.dependency_overrides[SessionManager.get_db] = lambda: MagicMock()
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_signup_missing_device_id_header(client):
    """Verify 400 Bad Request when X-Device-Id header is missing."""
    today = date.today()
    valid_date = f"{today.year - 20:04d}-01-01"
    payload = {
        "nick_name": "testuser",
        "email": "test@example.com",
        "password": "Password1!",
        "accept_terms": True,
        "term_code": "TERMS_OF_SERVICE",
        "term_version": 1,
        "born_date": valid_date,
    }
    response = client.post(
        "/api/v1/signup/user",
        json=payload,
        headers={"User-Agent": "Mozilla/5.0"},
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data["status"] == "ERROR"
    assert EResponseAuth.SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND.id in data["errors"]


def test_signup_terms_not_accepted(client):
    """Verify 400 Bad Request when terms are not accepted."""
    today = date.today()
    valid_date = f"{today.year - 20:04d}-01-01"
    payload = {
        "nick_name": "testuser",
        "email": "test@example.com",
        "password": "Password1!",
        "accept_terms": False,
        "term_code": "TERMS_OF_SERVICE",
        "term_version": 1,
        "born_date": valid_date,
    }
    response = client.post(
        "/api/v1/signup/user",
        json=payload,
        headers={
            "User-Agent": "Mozilla/5.0",
            "X-Device-Id": "device-123",
            "X-Forwarded-For": "192.168.1.1",
        },
    )
    assert response.status_code == HTTPStatus.BAD_REQUEST
    data = response.json()
    assert data["status"] == "ERROR"
    assert EResponseAuth.SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED.id in data["errors"]
