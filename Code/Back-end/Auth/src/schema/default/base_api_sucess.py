from schema.default.base_api_response import BaseApiResponse

class BaseApiSuccess(BaseApiResponse):
    """
        BaseApiSuccess class represents a successful response with a message, data, and status code.
    """
    message: str = "executed with success"
    status: str = "success"
