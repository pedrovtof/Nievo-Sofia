from pydantic import BaseModel, Field, EmailStr

class SignupUserRequest(BaseModel):
    """Represents a request to sign up a new user."""
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=20, description="The user's password. Must be between 6 and 20 characters.")
    accept_terms: bool = Field(..., description="Indicates whether the user accepts the terms and conditions.")
