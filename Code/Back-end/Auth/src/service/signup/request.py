from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, EmailStr,PastDate

class SignupUserRequest(BaseModel):
    """Represents a request to sign up a new user."""
    nick_name: str = Field(..., min_length=1, max_length=150, description="The user's nickname. Must be between 1 and 150 characters.")
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=16, description="The user's password. Must be between 8 and 16 characters.")
    accept_terms: bool = Field(..., description="Indicates whether the user accepts the terms and conditions.")
    term_code: str =Field(..., min_length=1, max_length=50, description="The term code that the user accepts")
    term_version: int =Field(...,ge=1, description="The term version that the user accepts.")
    born_date: PastDate = Field(..., description="The user's birth date (YYYY-MM-DD)")

    client_ip: Optional[str] = Field(default=None, exclude=True)
    x_device_id: Optional[str] = Field(default=None, exclude=True)
    user_agent: Optional[str] = Field(default=None, exclude=True)
