from http import HTTPStatus
from contracts.default.base_api_error import BaseApiError
from contracts.default.base_api_sucess import BaseApiSuccess
from contracts.default.base_api_sucess import BaseApiResponse
from contracts.request.v1.signup_request import SignupRequest

class AuthService:
    """
        AuthService class provides authentication-related services, such as user registration.
    """

    async def signup(self, request: SignupRequest) -> BaseApiResponse:
        """
            Registers a new user with the SignupRequest.
        """

        response = BaseApiSuccess(
            message="User registered successfully.",
            status_code=HTTPStatus.ACCEPTED,
            status="success"
        )

        return await response.to_json()