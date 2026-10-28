"""HTTP route controller for user registration endpoints."""
from fastapi import APIRouter, Depends
from schema.default.base_api_response import BaseApiResponse
from service.signup.request import SignupUserRequest
from service.signup.service import SignupService

router = APIRouter()

@router.post(
    path="/user",
    summary="Registrar usuário",
    description="Endpoint para registrar um novo usuário.",
    response_description="Retorna uma mensagem de sucesso e ou erro.",
    response_model=BaseApiResponse,
)
async def signup(
    request: SignupUserRequest,
    signup_service: SignupService = Depends(SignupService),
):
    """Handle user registration requests and delegate execution to SignupService."""
    return await signup_service.signup_user(request)
