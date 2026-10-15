from http import HTTPStatus
from fastapi.responses import JSONResponse

class BaseApiResponse:
    """
        BaseApiResponse class represents a generic API response with a message, data, and status code.
    """
    def __init__(self, message: str, data: dict, status_code: HTTPStatus, status: str):
        self.message = message or None
        self.data = data or None
        self.status_code = status_code or None
        self.status = status or None

    async def to_json(self) -> JSONResponse:
        "Structures the response as a json object."
        return JSONResponse(
            status_code=self.status_code,
            content={
                "status": self.status,
                "message": self.message,
                "data": self.data,
            }
        )
    