"""Application service handling user registration workflows."""
from http import HTTPStatus

from fastapi import Depends
from fastapi.responses import JSONResponse
from repositories.user import UserRepository
from repositories.user_agreements import UserAgreementsRepository
from repositories.device import DeviceRepository
from repositories.terms import TermsRepository
from schema.default.base_api_sucess import BaseApiSuccess
from schema.default.base_api_response import BaseApiResponse
from schema.default.base_api_error import BaseApiError
from service.signup.request import SignupUserRequest
from core.logging import CustomLogger
from core.enum.Eresponse_auth import EResponseAuth
from core.encryption import Encryption

class SignupService:
    """Provides authentication-related onboarding services such as user registration."""

    def __init__(self, 
            user_repository: UserRepository = Depends(UserRepository),
            user_agreement_repository: UserAgreementsRepository = Depends(UserAgreementsRepository),
            device_repository: DeviceRepository = Depends(DeviceRepository),
            terms_repository: TermsRepository = Depends(TermsRepository),
            encryption_service: Encryption = Depends(Encryption)
        ) -> None:
        """Initialize SignupService with injected repositories and password encryption service."""
        self._user_repository = user_repository
        self._user_agreement_repository = user_agreement_repository
        self._device_repository = device_repository
        self._terms_repository = terms_repository
        self._encryption_service = encryption_service

    async def signup_user(self, request: SignupUserRequest) -> JSONResponse:
        """Validate signup constraints, persist user, terms agreement, and device, and return HTTP 201."""

        response : BaseApiResponse = None

        if request.client_ip is None:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.message
            )

            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=response.model_dump(mode="json"),
            )

        if request.user_agent is None:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND.message
            )

            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=response.model_dump(mode="json"),
            )

        if request.x_device_id is None:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND.message
            )

            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=response.model_dump(mode="json"),
            )

        if request.accept_terms is not True:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED.message
            )

            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=response.model_dump(mode="json"),
            )

        user = await self._user_repository.get_by_mail(request.email)
        if user:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_ALREADY_EXISTS.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_ALREADY_EXISTS.message
            )

            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=response.model_dump(mode="json"),
            )

        term = await self._terms_repository.get_by_tag_and_version(request.term_code, request.term_version)
        if not term:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_TERM_INVALID.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_TERM_INVALID.message
            )

            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=response.model_dump(mode="json"),
            )

        valid_password = await self._encryption_service.validate_password(request.password)
        if not valid_password:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_PASSWORD_INVALID.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_PASSWORD_INVALID.message
            )

            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=response.model_dump(mode="json"),
            )
        
        hash_password = await self._encryption_service.encrypt_password(request.password)

        new_user = await self._user_repository.create(
            request.nick_name,
            request.email,
            hash_password
        )
        if not new_user:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER.message
            )
            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=response.model_dump(mode="json"),
            )

        new_user_agreement = await self._user_agreement_repository.create(
            new_user.id,
            term.id
        )
        if not new_user_agreement:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_AGREEMENTS.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_AGREEMENTS.message
            )

            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=response.model_dump(mode="json"),
            )

        new_device = await self._device_repository.create(
            new_user.id,
            request.x_device_id,
            ip_list= [request.client_ip],
            user_agent=request.user_agent
        )
        if not new_device:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_DEVICE.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_DEVICE.message
            )

            return JSONResponse(
                status_code=HTTPStatus.BAD_REQUEST,
                content=response.model_dump(mode="json"),
            )
        
        response = BaseApiSuccess(
            message="User registered successfully.",
        )

        return JSONResponse(
            status_code=HTTPStatus.CREATED,
            content=response.model_dump(mode="json"),
        )
