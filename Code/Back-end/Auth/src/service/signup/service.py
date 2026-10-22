from http import HTTPStatus
from fastapi.responses import JSONResponse

from schema.default.base_api_response import BaseApiResponse
from schema.default.base_api_sucess import BaseApiSuccess
from service.signup.request import SignupRequest

class SignupService:
    """
        SignupService class provides authentication-related services, such as user registration.
    """

    async def signup(self, request: SignupRequest) -> BaseApiResponse:
        """
            Registers a new user with the SignupRequest.
        """

        response = BaseApiSuccess(
            message="User registered successfully.",
            status="success"
        )

        return JSONResponse(
            status_code=HTTPStatus.ACCEPTED, 
            content=response.model_dump(mode="json")
        )