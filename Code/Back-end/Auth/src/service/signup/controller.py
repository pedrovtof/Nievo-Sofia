"""HTTP route controller for user registration endpoints."""

from fastapi import APIRouter, Depends, Header, Request
from schema.default.base_api_response import BaseApiResponse
from typing import Optional
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
    request: Request,
    request_contract: SignupUserRequest,
    signup_service: SignupService = Depends(SignupService),
    x_forwarded_for: Optional[str] = Header(default=None),
    user_agent: str = Header(default=None),
    x_device_id: str = Header(default=None)
):
    """Handle user registration requests and delegate execution to SignupService."""
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else None

    request_contract.client_ip = client_ip
    request_contract.user_agent = user_agent
    request_contract.x_device_id = x_device_id
    return await signup_service.signup_user(request_contract)
