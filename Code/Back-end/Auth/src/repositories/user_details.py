"""Repository providing persistence operations for the member.user_details database table."""
import datetime
from typing import Optional
import uuid

from contracts.entities.user_details import UserDetails
from core.database.session_manager import SessionManager
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from contracts.interface.Irepositories import IRepositories


class UserDetailsRepository(IRepositories):
    """Data access repository responsible for querying and persisting UserDetails entities."""

    def __init__(self, db_session: Session = Depends(SessionManager.get_db)) -> None:
            """Initialize the repository with an active SQLAlchemy database session."""
            self.db = db_session
    
    async def get_by_id(self, detail_id: uuid.UUID) -> Optional[UserDetails]:
        """Retrieve a user details record by its unique UUID identifier."""
        statement = select(UserDetails).where(UserDetails.id == detail_id)
        return self.db.scalars(statement).first()

    async def create_without_commit(self, 
            session: Session,
            user_id: uuid.UUID,
            born_date: datetime,
        ) -> UserDetails | bool:
        """Create a new UserDetails entity in the database without committing the transaction."""
        user_detail = UserDetails(
            user_id=user_id,
            born_date=born_date
        )
        try:
            session.add(user_detail)
            session.flush()
            return user_detail, True
        except Exception as e:
            return str(f"Failed to create user details without commit. {e}"), False

    async def create(self,
            born_date: datetime,
            user_id: uuid.UUID,
        ) -> UserDetails:
        """Persist a new UserDetail entity in the database and return the refreshed record."""
        user_detail = UserDetails(born_date=born_date, user_id=user_id)
        try:
            self.db.add(user_detail)
            self.db.commit()
            self.db.refresh(user_detail)
            return user_detail
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to create user details. {e}")

    def update(self, user_details: UserDetails) -> UserDetails:
        """Commit modifications to an existing UserDetail entity and return the refreshed record."""
        try:
            self.db.add(user_details)
            self.db.commit()
            self.db.refresh(user_details)
            return user_details
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Failed to update user details. {e}")
