from http import HTTPStatus

from contracts.default.base_api_response import BaseApiResponse

class BaseApiError(BaseApiResponse):
    """
        BaseApiError class represents an error response with a message, data, and status code.
    """
    def __init__(self, message: str = "An error occurred", data: dict = None, status_code: HTTPStatus = HTTPStatus.BAD_REQUEST, status: str = "error", errors: list = []):
        super().__init__(message=message, data=data or {}, status_code=status_code, status=status)
        self.errors = errors

    def to_json(self) -> dict:
        "Structures the error response as a json object."
        response = super().to_json()
        response["errors"] = self.errors
        response["count"] = len(self.errors)
        return response