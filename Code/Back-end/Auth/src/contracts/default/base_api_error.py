from http import HTTPStatus
from fastapi.responses import JSONResponse

from contracts.default.base_api_response import BaseApiResponse

class BaseApiError(BaseApiResponse):
    """
        BaseApiError class represents an error response with a message, data, and status code.
    """
    def __init__(self, message: str = "An error occurred", data: dict = None, status_code: HTTPStatus = HTTPStatus.BAD_REQUEST, status: str = "error", errors: list = []):
        super().__init__(message=message, data=data or None, status_code=status_code, status=status)
        self.errors = errors

    async def to_json(self) -> JSONResponse:
        "Structures the error response as a json object."
        return JSONResponse(
            status_code=self.status_code,
            content={
                "status": self.status,
                "message": self.message,
                "data": self.data,
            "errors": self.errors,
        })