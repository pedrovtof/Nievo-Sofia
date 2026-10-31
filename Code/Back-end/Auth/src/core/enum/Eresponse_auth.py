"""Enumeration catalog of domain error codes and messages for the Auth service."""
from enum import Enum
class EResponseAuth(Enum):
    """
        Use the template
        SERVICE + STATUS_HTTP + DEF + MESSAGE
    """
    def __init__(self, id_num, message):
            """Initialize an authentication response enum member with its code ID and message."""
            self.id = id_num
            self.message = message

    SIGNUP_400_SIGNUP_USER_USER_ALREADY_EXISTS = (1,"Email or username invalid")

    SIGNUP_400_SIGNUP_USER_PASSWORD_INVALID = (2,"The password must contain a single digit from 0 to 9, lowercase letter, no space,uppercase letter, special character and a size between 8 and 16")

    SIGNUP_400_SIGNUP_USER_TERM_INVALID = (3,"Invalid term code or version")

    SIGNUP_400_SIGNUP_USER_NOT_CREATED_AGREEMENTS = (3,"Sorry! that user could not be created, please try again later")

    SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER = (3,"Sorry! that user could not be created, please try again later")

    SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED = (4,"You must accept the terms and conditions to continue")

    SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND = (5,"The client IP address could not be determined")

    SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND = (6,"The user agent could not be determined")

    SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND = (7,"The device ID could not be determined")

    SIGNUP_400_SIGNUP_USER_NOT_CREATED_DEVICE = (8,"Sorry! that user could not be created, please try again later")

    SIGNUP_201_SIGNUP_USER_CREATED = (9,"User registered successfully.")

    SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER_DETAILS = (10,"Sorry! that user could not be created, please try again later")

    SIGNUP_400_SIGNUP_USER_WITH_INVALID_BIRTH_DATE = (11,"Please validate the born date")