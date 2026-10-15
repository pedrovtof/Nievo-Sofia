from http import HTTPStatus

class BaseApiResponse:
    """
        BaseApiResponse class represents a generic API response with a message, data, and status code.
    """
    def __init__(self, message: str, data: dict, status_code: HTTPStatus, status: str):
        self.message = message or None
        self.data = data or {}
        self.status_code = status_code or None
        self.status = status or None

    def to_json(self) -> dict:
        "Structures the response as a json object."
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
        }
    