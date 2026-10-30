"""Application service handling user registration workflows."""
from http import HTTPStatus

from fastapi import Depends
from repositories.user import UserRepository
from repositories.user_agreements import UserAgreementsRepository
from repositories.device import DeviceRepository
from repositories.terms import TermsRepository
from schema.default.base_api_sucess import BaseApiSuccess
from schema.default.base_api_response import BaseApiResponse
from schema.default.base_api_error import BaseApiError
from service.signup.request import SignupUserRequest
from core.database.session_manager import SessionManager
from datetime import datetime
from sqlalchemy.orm import Session
from core.logging import CustomLogger
from core.enum.Eresponse_auth import EResponseAuth
from core.encryption import Encryption
from repositories.user_details import UserDetailsRepository
import os

custom_logger= CustomLogger(__name__)

class SignupService:
    """Provides authentication-related onboarding services such as user registration."""

    def __init__(self, 
            db_session: Session = Depends(SessionManager.get_db),
            user_repository: UserRepository = Depends(UserRepository),
            user_agreement_repository: UserAgreementsRepository = Depends(UserAgreementsRepository),
            user_details_repository : UserDetailsRepository = Depends(UserDetailsRepository),
            device_repository: DeviceRepository = Depends(DeviceRepository),
            terms_repository: TermsRepository = Depends(TermsRepository),
            encryption_service: Encryption = Depends(Encryption),
        ) -> None:
        """Initialize SignupService with injected repositories and password encryption service."""
        self._logger = custom_logger
        self._db_transaction = db_session
        self._user_repository = user_repository
        self._user_agreement_repository = user_agreement_repository
        self._user_details_repository = user_details_repository
        self._device_repository = device_repository
        self._terms_repository = terms_repository
        self._encryption_service = encryption_service

    async def signup_user(self, request: SignupUserRequest):
        """Validate signup constraints, persist user, terms agreement, and device, and return HTTP 201."""

        response : BaseApiResponse = None

        if request.client_ip is None:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_IP_NOT_FOUND.message
            )
            return HTTPStatus.BAD_REQUEST, response

        if request.user_agent is None:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_AGENT_NOT_FOUND.message
            )
            return HTTPStatus.BAD_REQUEST, response

        if request.x_device_id is None:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_DEVICE_ID_NOT_FOUND.message
            )
            return HTTPStatus.BAD_REQUEST,response

        if request.accept_terms is not True:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_TERMS_NOT_ACCEPTED.message
            )
            return HTTPStatus.BAD_REQUEST, response

        born_date = datetime.strptime(str(request.born_date), "%Y-%m-%d")
        data_diff = abs(born_date - datetime.now())
        years_diff, _ = divmod(data_diff.days, 365)

        if years_diff < int(os.getenv("MIN_AGE_FOR_ACCOUNT",6)) or years_diff > int(os.getenv("MAX_AGE_FOR_ACCOUNT",110)):
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_WITH_INVALID_BIRTH_DATE.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_WITH_INVALID_BIRTH_DATE.message
            )
            return HTTPStatus.BAD_REQUEST,response
        

        user = await self._user_repository.get_by_mail(request.email)
        if user:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_ALREADY_EXISTS.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_USER_ALREADY_EXISTS.message
            )
            return HTTPStatus.BAD_REQUEST,response

        term = await self._terms_repository.get_by_tag_and_version(request.term_code, request.term_version)
        if not term:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_TERM_INVALID.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_TERM_INVALID.message
            )
            return HTTPStatus.BAD_REQUEST,response

        valid_password = await self._encryption_service.validate_password(request.password)
        if not valid_password:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_PASSWORD_INVALID.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_PASSWORD_INVALID.message
            )
            return HTTPStatus.BAD_REQUEST, response

        hash_password = await self._encryption_service.encrypt_password(request.password)

        sucess_transaction = False

        new_user,sucess_transaction = await self._user_repository.create_without_commit(
            self._db_transaction,
            request.nick_name,
            request.email,
            hash_password
        )
        if not new_user or sucess_transaction == False :
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER.message
            )
            self._db_transaction.rollback()
            return HTTPStatus.BAD_REQUEST, response

        new_user_details, sucess_transaction = await self._user_details_repository.create_without_commit(
            self._db_transaction,
            new_user.id,
            request.born_date
        )
        if not new_user_details or sucess_transaction == False :
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER_DETAILS.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_USER_DETAILS.message
            )
            self._db_transaction.rollback()
            return HTTPStatus.BAD_REQUEST, response

        new_user_agreement,sucess_transaction = await self._user_agreement_repository.create_without_commit(
            self._db_transaction,
            new_user.id,
            term.id
        )
        if not new_user_agreement or sucess_transaction == False:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_AGREEMENTS.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_AGREEMENTS.message
            )
            self._db_transaction.rollback()
            return HTTPStatus.BAD_REQUEST, response

        new_device,sucess_transaction = await self._device_repository.create_without_commit(
            self._db_transaction,
            new_user.id,
            request.x_device_id,
            ip_list= [request.client_ip],
            user_agent=request.user_agent
        )
        if not new_device or sucess_transaction == False:
            response = BaseApiError(
                errors=[EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_DEVICE.id],
                message=EResponseAuth.SIGNUP_400_SIGNUP_USER_NOT_CREATED_DEVICE.message
            )
            self._db_transaction.rollback()
            return HTTPStatus.BAD_REQUEST, response

        self._db_transaction.commit()

        response = BaseApiSuccess(
            message=EResponseAuth.SIGNUP_201_SIGNUP_USER_CREATED.message,
        )
        return HTTPStatus.CREATED, response
