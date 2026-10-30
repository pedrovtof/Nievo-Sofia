"""Unit tests covering every return outcome in SignupService.signup_user."""
from datetime import date
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock
import uuid
import pytest

from core.enum.Eresponse_auth import EResponseAuth
from schema.default.base_api_error import BaseApiError
from schema.default.base_api_sucess import BaseApiSuccess
from service.signup.request import SignupUserRequest
from service.signup.service import SignupService


@pytest.fixture
def mock_dependencies():
    """Build mock dependencies for SignupService initialization."""
    db_session = MagicMock()
    user_repo = MagicMock()
    user_repo.get_by_mail = AsyncMock()
    user_repo.create_without_commit = AsyncMock()

    user_agreement_repo = MagicMock()
    user_agreement_repo.create_without_commit = AsyncMock()

    user_details_repo = MagicMock()
    user_details_repo.create_without_commit = AsyncMock()

    device_repo = MagicMock()
    device_repo.create_without_commit = AsyncMock()

    terms_repo = MagicMock()
    terms_repo.get_by_tag_and_version = AsyncMock()

    encryption_service = MagicMock()
    encryption_service.validate_password = AsyncMock()
    encryption_service.encrypt_password = AsyncMock()

    return {
        "db_session": db_session,
        "user_repository": user_repo,
        "user_agreement_repository": user_agreement_repo,
        "user_details_repository": user_details_repo,
        "device_repository": device_repo,
        "terms_repository": terms_repo,
        "encryption_service": encryption_service,
    }


@pytest.fixture
def signup_service(mock_dependencies):
    """Instantiate SignupService with mocked dependencies."""
    return SignupService(**mock_dependencies)


@pytest.fixture
def valid_signup_request():
    """Build a valid SignupUserRequest object."""
    today = date.today()
    valid_date = date(today.year - 20, today.month, today.day)
    return SignupUserRequest(
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


@pytest.mark.anyio
async def test_signup_user_returns_validator_failure(signup_service, mock_dependencies, monkeypatch, valid_signup_request):
    """1. Return option: SignupUserValidator returns failure status and BaseApiError."""
    mock_validate = AsyncMock(
        return_value=(
            HTTPStatus.BAD_REQUEST,
            BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.message,
            ),
        )
    )
    monkeypatch.setattr("service.signup.service.SignupUserValidator.validate_request", mock_validate)

    status, response = await signup_service.signup_user(valid_signup_request)

    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.message
    mock_dependencies["user_repository"].get_by_mail.assert_not_called()


@pytest.mark.anyio
async def test_signup_user_returns_user_already_exists(signup_service, mock_dependencies, monkeypatch, valid_signup_request):
    """2. Return option: Email already registered returns SIGNUP_400_SIGNUP_USER_USER_ALREADY_EXISTS."""
    monkeypatch.setattr(
        "service.signup.service.SignupUserValidator.validate_request",
        AsyncMock(return_value=(None, None)),
    )
    mock_dependencies["user_repository"].get_by_mail.return_value = MagicMock()

    status, response = await signup_service.signup_user(valid_signup_request)

    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_ALREADY_EXISTS.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_ALREADY_EXISTS.message
    mock_dependencies["terms_repository"].get_by_tag_and_version.assert_not_called()


@pytest.mark.anyio
async def test_signup_user_returns_term_invalid(signup_service, mock_dependencies, monkeypatch, valid_signup_request):
    """3. Return option: Term lookup returns None, returning SIGNUP_400_SIGNUP_USER_TERM_INVALID."""
    monkeypatch.setattr(
        "service.signup.service.SignupUserValidator.validate_request",
        AsyncMock(return_value=(None, None)),
    )
    mock_dependencies["user_repository"].get_by_mail.return_value = None
    mock_dependencies["terms_repository"].get_by_tag_and_version.return_value = None

    status, response = await signup_service.signup_user(valid_signup_request)

    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_TERM_INVALID.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_TERM_INVALID.message
    mock_dependencies["encryption_service"].validate_password.assert_not_called()


@pytest.mark.anyio
async def test_signup_user_returns_password_invalid(signup_service, mock_dependencies, monkeypatch, valid_signup_request):
    """4. Return option: Password complexity validation fails, returning SIGNUP_400_SIGNUP_USER_PASSWORD_INVALID."""
    monkeypatch.setattr(
        "service.signup.service.SignupUserValidator.validate_request",
        AsyncMock(return_value=(None, None)),
    )
    mock_dependencies["user_repository"].get_by_mail.return_value = None
    mock_term = MagicMock()
    mock_term.id = 1
    mock_dependencies["terms_repository"].get_by_tag_and_version.return_value = mock_term
    mock_dependencies["encryption_service"].validate_password.return_value = False

    status, response = await signup_service.signup_user(valid_signup_request)

    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_PASSWORD_INVALID.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_PASSWORD_INVALID.message
    mock_dependencies["encryption_service"].encrypt_password.assert_not_called()


@pytest.mark.anyio
async def test_signup_user_returns_not_created_user(signup_service, mock_dependencies, monkeypatch, valid_signup_request):
    """5. Return option: User persistence fails, triggering rollback and returning SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER."""
    monkeypatch.setattr(
        "service.signup.service.SignupUserValidator.validate_request",
        AsyncMock(return_value=(None, None)),
    )
    mock_dependencies["user_repository"].get_by_mail.return_value = None
    mock_term = MagicMock()
    mock_term.id = 1
    mock_dependencies["terms_repository"].get_by_tag_and_version.return_value = mock_term
    mock_dependencies["encryption_service"].validate_password.return_value = True
    mock_dependencies["encryption_service"].encrypt_password.return_value = "hashed_pw"

    # User creation failure
    mock_dependencies["user_repository"].create_without_commit.return_value = (None, False)

    status, response = await signup_service.signup_user(valid_signup_request)

    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER.message
    mock_dependencies["db_session"].rollback.assert_called_once()
    mock_dependencies["user_details_repository"].create_without_commit.assert_not_called()


@pytest.mark.anyio
async def test_signup_user_returns_not_created_user_details(signup_service, mock_dependencies, monkeypatch, valid_signup_request):
    """6. Return option: User details persistence fails, triggering rollback and returning SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER_DETAILS."""
    monkeypatch.setattr(
        "service.signup.service.SignupUserValidator.validate_request",
        AsyncMock(return_value=(None, None)),
    )
    mock_dependencies["user_repository"].get_by_mail.return_value = None
    mock_term = MagicMock()
    mock_term.id = 1
    mock_dependencies["terms_repository"].get_by_tag_and_version.return_value = mock_term
    mock_dependencies["encryption_service"].validate_password.return_value = True
    mock_dependencies["encryption_service"].encrypt_password.return_value = "hashed_pw"

    mock_user = MagicMock()
    mock_user.id = uuid.uuid4()
    mock_dependencies["user_repository"].create_without_commit.return_value = (mock_user, True)

    # User details creation failure
    mock_dependencies["user_details_repository"].create_without_commit.return_value = (None, False)

    status, response = await signup_service.signup_user(valid_signup_request)

    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER_DETAILS.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER_DETAILS.message
    mock_dependencies["db_session"].rollback.assert_called_once()
    mock_dependencies["user_agreement_repository"].create_without_commit.assert_not_called()


@pytest.mark.anyio
async def test_signup_user_returns_not_created_agreements(signup_service, mock_dependencies, monkeypatch, valid_signup_request):
    """7. Return option: User agreement persistence fails, triggering rollback and returning SIGNUP_400_SIGNUP_USER_NOT_CREATED_AGREEMENTS."""
    monkeypatch.setattr(
        "service.signup.service.SignupUserValidator.validate_request",
        AsyncMock(return_value=(None, None)),
    )
    mock_dependencies["user_repository"].get_by_mail.return_value = None
    mock_term = MagicMock()
    mock_term.id = 1
    mock_dependencies["terms_repository"].get_by_tag_and_version.return_value = mock_term
    mock_dependencies["encryption_service"].validate_password.return_value = True
    mock_dependencies["encryption_service"].encrypt_password.return_value = "hashed_pw"

    mock_user = MagicMock()
    mock_user.id = uuid.uuid4()
    mock_dependencies["user_repository"].create_without_commit.return_value = (mock_user, True)

    mock_details = MagicMock()
    mock_dependencies["user_details_repository"].create_without_commit.return_value = (mock_details, True)

    # Agreement creation failure
    mock_dependencies["user_agreement_repository"].create_without_commit.return_value = (None, False)

    status, response = await signup_service.signup_user(valid_signup_request)

    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_AGREEMENTS.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_AGREEMENTS.message
    mock_dependencies["db_session"].rollback.assert_called_once()
    mock_dependencies["device_repository"].create_without_commit.assert_not_called()


@pytest.mark.anyio
async def test_signup_user_returns_not_created_device(signup_service, mock_dependencies, monkeypatch, valid_signup_request):
    """8. Return option: Device persistence fails, triggering rollback and returning SIGNUP_400_SIGNUP_USER_NOT_CREATED_DEVICE."""
    monkeypatch.setattr(
        "service.signup.service.SignupUserValidator.validate_request",
        AsyncMock(return_value=(None, None)),
    )
    mock_dependencies["user_repository"].get_by_mail.return_value = None
    mock_term = MagicMock()
    mock_term.id = 1
    mock_dependencies["terms_repository"].get_by_tag_and_version.return_value = mock_term
    mock_dependencies["encryption_service"].validate_password.return_value = True
    mock_dependencies["encryption_service"].encrypt_password.return_value = "hashed_pw"

    mock_user = MagicMock()
    mock_user.id = uuid.uuid4()
    mock_dependencies["user_repository"].create_without_commit.return_value = (mock_user, True)

    mock_details = MagicMock()
    mock_dependencies["user_details_repository"].create_without_commit.return_value = (mock_details, True)

    mock_agreement = MagicMock()
    mock_dependencies["user_agreement_repository"].create_without_commit.return_value = (mock_agreement, True)

    # Device creation failure
    mock_dependencies["device_repository"].create_without_commit.return_value = (None, False)

    status, response = await signup_service.signup_user(valid_signup_request)

    assert status == HTTPStatus.BAD_REQUEST
    assert response.errors == [EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_DEVICE.id]
    assert response.message == EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_DEVICE.message
    mock_dependencies["db_session"].rollback.assert_called_once()
    mock_dependencies["db_session"].commit.assert_not_called()


@pytest.mark.anyio
async def test_signup_user_returns_created_success(signup_service, mock_dependencies, monkeypatch, valid_signup_request):
    """9. Return option: Successful registration flow committing transaction and returning HTTP 201 BaseApiSuccess."""
    monkeypatch.setattr(
        "service.signup.service.SignupUserValidator.validate_request",
        AsyncMock(return_value=(None, None)),
    )
    mock_dependencies["user_repository"].get_by_mail.return_value = None

    mock_term = MagicMock()
    mock_term.id = 1
    mock_dependencies["terms_repository"].get_by_tag_and_version.return_value = mock_term

    mock_dependencies["encryption_service"].validate_password.return_value = True
    mock_dependencies["encryption_service"].encrypt_password.return_value = "hashed_pw"

    mock_user = MagicMock()
    mock_user.id = uuid.uuid4()
    mock_dependencies["user_repository"].create_without_commit.return_value = (mock_user, True)

    mock_details = MagicMock()
    mock_dependencies["user_details_repository"].create_without_commit.return_value = (mock_details, True)

    mock_agreement = MagicMock()
    mock_dependencies["user_agreement_repository"].create_without_commit.return_value = (mock_agreement, True)

    mock_device = MagicMock()
    mock_dependencies["device_repository"].create_without_commit.return_value = (mock_device, True)

    status, response = await signup_service.signup_user(valid_signup_request)

    assert status == HTTPStatus.CREATED
    assert isinstance(response, BaseApiSuccess)
    assert response.message == EResponseAuth.SIGNUP_201_SIGNUP_USER_CREATED.message
    mock_dependencies["db_session"].commit.assert_called_once()
