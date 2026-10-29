from schema.default.base_api_response import BaseApiResponse
from core.enum.Estatus_base_api import EStatusBaseApi

class BaseApiSuccess(BaseApiResponse):
    """
        BaseApiSuccess class represents a successful response with a message, data, and status code.
    """
    message: str = "executed with success"
    status: EStatusBaseApi = EStatusBaseApi.SUCESS.name
