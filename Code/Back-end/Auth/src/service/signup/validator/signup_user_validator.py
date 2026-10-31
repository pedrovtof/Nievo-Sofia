"""Validation components for user registration requests."""
from datetime import datetime
from http import HTTPStatus
import os

from service.signup.request import SignupUserRequest
from core.enum.Eresponse_auth import EResponseAuth
from schema.default.base_api_error import BaseApiError

class SignupUserValidator:
    """Validates incoming user registration payload and metadata requirements."""

    @classmethod
    async def validate_request(cls, request: SignupUserRequest):
        """Validate client IP, user agent, device ID, terms acceptance, and age constraints."""
        if request.client_ip is None:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.message
            )
            return HTTPStatus.BAD_REQUEST, response

        if request.user_agent is None:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND.message
            )
            return HTTPStatus.BAD_REQUEST, response

        if request.x_device_id is None:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND.message
            )
            return HTTPStatus.BAD_REQUEST, response

        if request.accept_terms is not True:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED.message
            )
            return HTTPStatus.BAD_REQUEST, response

        born_date = datetime.strptime(str(request.born_date), "%Y-%m-%d")
        data_diff = abs(born_date - datetime.now())
        years_diff, _ = divmod(data_diff.days, 365)

        if years_diff < int(os.getenv("MIN_AGE_FOR_ACCOUNT", 6)) or years_diff > int(os.getenv("MAX_AGE_FOR_ACCOUNT", 110)):
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_WITH_INVALID_BIRTH_DATE.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_WITH_INVALID_BIRTH_DATE.message
            )
            return HTTPStatus.BAD_REQUEST, response

        return None, None
