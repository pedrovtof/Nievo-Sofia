"""Repository providing persistence operations for the member.user database table."""
from typing import Optional
import uuid

from contracts.entities.user import User
from core.database.session_manager import SessionManager
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from contracts.interface.Irepositories import IRepositories


class UserRepository(IRepositories):
    """Data access repository responsible for querying and persisting User entities."""

    def __init__(self, db_session: Session = Depends(SessionManager.get_db)) -> None:
        """Initialize the repository with an active SQLAlchemy database session."""
        self.db = db_session

    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """Retrieve a user record by its unique UUID identifier."""
        statement = select(User).where(User.id == user_id)
        return self.db.scalars(statement).first()

    async def get_by_mail(self, user_email: str) -> Optional[User]:
        """Retrieve a user record by its unique UUID identifier."""
        statement = select(User).where(User.email == user_email)
        return self.db.scalars(statement).first()

    async def create(self, nick_name,email,password) -> User:
        """Persist a new User entity in the database and return the refreshed record."""
        user = User(nick_name=nick_name, email=email, password=password)
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception:
            self.db.rollback()
            raise

    def update(self, user: User) -> User:
        """Commit modifications to an existing User entity and return the refreshed record."""
        try:
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception:
            self.db.rollback()
            raise
