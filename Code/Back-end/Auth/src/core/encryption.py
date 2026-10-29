"""Password policy validation and bcrypt hashing utilities for authentication."""
import bcrypt
import os
from core.logging import CustomLogger
import re 
from fastapi import Depends

class Encryption:
    """Provides password complexity validation, bcrypt hashing, and hash verification."""

    def __init__(self):
        """Initialize encryption encoding and password regex rules from environment variables."""
        self._encode = os.getenv("ENCODE_ENCRYPT_PASSWORD", None)
        self._regex_for_valid_password = os.getenv("REGEX_FOR_PASSWORD", None)
        self._logger = CustomLogger("Encryption")

        if not self._encode or not self._regex_for_valid_password:
            raise Exception("You must inform the ENCODE_ENCRYPT_PASSWORD/REGEX_FOR_PASSWORD")

    async def validate_password(self, password) -> bool:
        """Validate whether a plain-text password satisfies the configured complexity regex."""
        if re.fullmatch(self._regex_for_valid_password, password):
            return True
        else:
            return False

    async def check_password(self,password,hash )-> bool:
        """Verify a plain-text password attempt against a stored bcrypt hash."""
        attemp_password = password.encode('utf-8')

        if bcrypt.checkpw(attemp_password, hash):
            return True
        else:
            False

    async def encrypt_password(self, password) -> str:
        """Hash a plain-text password with bcrypt and return its decoded string representation."""
        password_for_utf = password.encode(self._encode)
        try:
            hash = bcrypt.hashpw(password_for_utf, bcrypt.gensalt())
            return str(hash.decode(self._encode))
        except Exception as e:
            self._logger.error(message=f"There was an error during the encrypt password {e}")
            raise Exception("There was an error during the encrypt password")

  
