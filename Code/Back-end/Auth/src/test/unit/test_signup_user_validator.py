"""Unit tests for SignupUserValidator."""
from datetime import date
from http import HTTPStatus
import pytest

from core.enum.Eresponse_auth import EResponseAuth
from service.signup.request import SignupUserRequest
from service.signup.validator.signup_user_validator import SignupUserValidator


@pytest.mark.anyio
async def test_validate_request_missing_client_ip():
    """Verify validation failure when client IP is missing."""
    request = SignupUserRequest(
        nick_name="testuser",
        email="test@example.com",
        password="Password1!",
        accept_terms=True,
        term_code="TERMS_OF_SERVICE",
        term_version=1,
        born_date=date(2000, 1, 1),
        client_ip=None,
        user_agent="Mozilla/5.0",
        x_device_id="device-123",
    )
    status, response = await SignupUserValidator.validate_request(request)
    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.message


@pytest.mark.anyio
async def test_validate_request_missing_user_agent():
    """Verify validation failure when user agent is missing."""
    request = SignupUserRequest(
        nick_name="testuser",
        email="test@example.com",
        password="Password1!",
        accept_terms=True,
        term_code="TERMS_OF_SERVICE",
        term_version=1,
        born_date=date(2000, 1, 1),
        client_ip="127.0.0.1",
        user_agent=None,
        x_device_id="device-123",
    )
    status, response = await SignupUserValidator.validate_request(request)
    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND.message


@pytest.mark.anyio
async def test_validate_request_missing_device_id():
    """Verify validation failure when x_device_id is missing."""
    request = SignupUserRequest(
        nick_name="testuser",
        email="test@example.com",
        password="Password1!",
        accept_terms=True,
        term_code="TERMS_OF_SERVICE",
        term_version=1,
        born_date=date(2000, 1, 1),
        client_ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        x_device_id=None,
    )
    status, response = await SignupUserValidator.validate_request(request)
    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND.message


@pytest.mark.anyio
async def test_validate_request_terms_not_accepted():
    """Verify validation failure when terms acceptance is false."""
    request = SignupUserRequest(
        nick_name="testuser",
        email="test@example.com",
        password="Password1!",
        accept_terms=False,
        term_code="TERMS_OF_SERVICE",
        term_version=1,
        born_date=date(2000, 1, 1),
        client_ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        x_device_id="device-123",
    )
    status, response = await SignupUserValidator.validate_request(request)
    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED.message


@pytest.mark.anyio
async def test_validate_request_age_too_young():
    """Verify validation failure when user age is below minimum age boundary."""
    today = date.today()
    too_young_date = date(today.year - 2, today.month, today.day)
    request = SignupUserRequest(
        nick_name="testuser",
        email="test@example.com",
        password="Password1!",
        accept_terms=True,
        term_code="TERMS_OF_SERVICE",
        term_version=1,
        born_date=too_young_date,
        client_ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        x_device_id="device-123",
    )
    status, response = await SignupUserValidator.validate_request(request)
    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_WITH_INVALID_BIRTH_DATE.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_WITH_INVALID_BIRTH_DATE.message


@pytest.mark.anyio
async def test_validate_request_age_too_old():
    """Verify validation failure when user age exceeds maximum age boundary."""
    today = date.today()
    too_old_date = date(today.year - 120, today.month, today.day)
    request = SignupUserRequest(
        nick_name="testuser",
        email="test@example.com",
        password="Password1!",
        accept_terms=True,
        term_code="TERMS_OF_SERVICE",
        term_version=1,
        born_date=too_old_date,
        client_ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        x_device_id="device-123",
    )
    status, response = await SignupUserValidator.validate_request(request)
    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_WITH_INVALID_BIRTH_DATE.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_WITH_INVALID_BIRTH_DATE.message


@pytest.mark.anyio
async def test_validate_request_valid():
    """Verify validation success when all parameters are valid."""
    today = date.today()
    valid_date = date(today.year - 25, today.month, today.day)
    request = SignupUserRequest(
        nick_name="testuser",
        email="test@example.com",
        password="Password1!",
        accept_terms=True,
        term_code="TERMS_OF_SERVICE",
        term_version=1,
        born_date=valid_date,
        client_ip="127.0.0.1",
        user_agent="Mozilla/5.0",
        x_device_id="device-123",
    )
    status, response = await SignupUserValidator.validate_request(request)
    assert status is None
    assert response is None
