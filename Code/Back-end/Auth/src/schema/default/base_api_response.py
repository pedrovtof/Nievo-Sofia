from typing import Any, Optional

from pydantic import BaseModel
from http import HTTPStatus
from core.enum.Estatus_base_api import EStatusBaseApi
from fastapi.responses import JSONResponse

class BaseApiResponse(BaseModel):
    """
        BaseApiResponse class represents a generic API response with a message, data, and status code.
    """
    message: Optional[str] = None                                                                                                                    
    data: Optional[dict[str, Any]] = None                                                                                                  
    status: Optional[EStatusBaseApi] = None