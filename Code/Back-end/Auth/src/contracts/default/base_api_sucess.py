from contracts.default.base_api_response import BaseApiResponse
from http import HTTPStatus

class BaseApiSuccess(BaseApiResponse):
    """
        BaseApiSuccess class represents a successful response with a message, data, and status code.
    """
    def __init__(self, message: str = "executed with success", data: dict = None, status_code: HTTPStatus = HTTPStatus.OK, status: str = "success"):
        super().__init__(message=message, data=data or None, status_code=status_code, status=status)
