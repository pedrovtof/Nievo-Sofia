"""Enumeration defining standardized status outcomes for API responses."""
from enum import Enum
class EStatusBaseApi(Enum):
    """Standardized response status values serialized in BaseApiResponse envelopes."""
    SUCESS = 1
    ERROR = 2
    WARNING = 3
