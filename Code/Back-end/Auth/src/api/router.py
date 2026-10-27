from fastapi import APIRouter
from service.signup import controller as v1_auth_controller

api_router = APIRouter()

api_router.include_router(v1_auth_controller.router, prefix="/v1/signup", tags=["auth"])
