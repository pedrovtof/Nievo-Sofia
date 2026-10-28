"""Application service handling user registration workflows."""
from http import HTTPStatus

from fastapi import Depends
from fastapi.responses import JSONResponse
from repositories.user import UserRepository
from schema.default.base_api_sucess import BaseApiSuccess
from service.signup.request import SignupUserRequest


class SignupService:
    """Provides authentication-related onboarding services such as user registration."""

    def __init__(self, user_repository: UserRepository = Depends(UserRepository)) -> None:
        """Initialize SignupService with an injected UserRepository instance."""
        self._user_repository = user_repository

    async def signup_user(self, request: SignupUserRequest) -> JSONResponse:
        """Process a user signup request and return an accepted API response envelope."""
        response = BaseApiSuccess(
            message="User registered successfully.",
            status="success",
        )

        return JSONResponse(
            status_code=HTTPStatus.ACCEPTED,
            content=response.model_dump(mode="json"),
        )
