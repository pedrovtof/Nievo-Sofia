from fastapi import APIRouter
from service.auth_service import AuthService
from contracts.default.base_api_sucess import BaseApiResponse
from contracts.request.v1.signup_request import SignupRequest

router = APIRouter()
auth_service = AuthService()

@router.post(
        path="/", 
        summary="Registrar usuário", 
        description="Endpoint para registrar um novo usuário.",
        response_description="Retorna uma mensagem de sucesso e os dados do usuário registrado.",
    )
async def signup(request: SignupRequest):
    return await auth_service.signup(request)