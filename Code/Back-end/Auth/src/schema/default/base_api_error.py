from typing import Any, Optional
from pydantic import Field

from schema.default.base_api_response import BaseApiResponse

class BaseApiError(BaseApiResponse):
    """
        BaseApiError class represents an error response with a message, data, and status code.
    """
    message: str = "An error occurred"
    status: str = "error"
    errors: Optional[list[Any]] = Field(default_factory=list)
