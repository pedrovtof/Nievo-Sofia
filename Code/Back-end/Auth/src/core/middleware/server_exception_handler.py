from http import HTTPStatus
from fastapi import Request

from core.logging import CustomLogger
from schema.default.base_api_error import BaseApiError
from fastapi.responses import JSONResponse


log = CustomLogger(__name__)

class ServerExceptionHandler:
    """
        ServerExceptionHandler class handles unhandled exceptions in the FastAPI application.
    """
    def __init__(self, request: Request, exception: Exception):
        self.request = request
        self.exception = exception

    async def handle_exception(self):
        """
            Handles the unhandled exception and returns a structured error response.
        """
        log.error(f"Unhandled exception occurred: request={self.request} exception={self.exception}")

        response = BaseApiError(                                                                                                                       
            message="Ops! Something went wrong. Try again later.",                                                                                           
            data={                                                                                                                                           
                "details": self.exception.__str__(),
                "method": self.request.method,
                "url": str(self.request.url)                                                                                                                
            },
            errors=["Internal Server Error"]
        )

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR, 
            content=response.model_dump(mode="json")
        )