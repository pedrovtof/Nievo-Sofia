from fastapi import APIRouter
from service.signup.service import SignupService
from schema.default.base_api_response import BaseApiResponse
from service.signup.request import SignupRequest

router = APIRouter()
signup_service = SignupService()

@router.post(
        path="/", 
        summary="Registrar usuário", 
        description="Endpoint para registrar um novo usuário.",
        response_description="Retorna uma mensagem de sucesso e os dados do usuário registrado.",
        response_model=BaseApiResponse
    )
async def signup(request: SignupRequest):
    return await signup_service.signup(request)
