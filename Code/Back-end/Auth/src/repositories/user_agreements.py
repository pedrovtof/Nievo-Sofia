"""Repository providing persistence operations for the signup.user_agreements database table."""
from typing import Optional
import uuid

from contracts.entities.user_agreements import UserAgreements
from core.database.session_manager import SessionManager
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from contracts.interface.Irepositories import IRepositories


class UserAgreementsRepository(IRepositories):
    """Data access repository responsible for querying and persisting User agreements entities."""

    def __init__(self, db_session: Session = Depends(SessionManager.get_db)) -> None:
        """Initialize the repository with an active SQLAlchemy database session."""
        self.db = db_session

    async def get_by_id(self, agreement_id: int) -> Optional[UserAgreements]:
        """Retrieve a user agreement record by its unique UUID identifier."""
        statement = select(UserAgreements).where(UserAgreements.id == agreement_id)
        return self.db.scalars(statement).first()

    async def create(self, user_id: uuid.UUID, term_id: int) -> UserAgreements:
        """Persist a new User agreement entity in the database and return the refreshed record."""
        user_agreement = UserAgreements(user_id=user_id, term_id=term_id)
        try:
            self.db.add(user_agreement)
            self.db.commit()
            self.db.refresh(user_agreement)
            return user_agreement
        except Exception:
            self.db.rollback()
            raise