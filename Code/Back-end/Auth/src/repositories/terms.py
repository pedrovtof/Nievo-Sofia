"""Repository providing persistence operations for the signup.term database table."""
from typing import Optional
import uuid

from contracts.entities.terms import Terms
from core.database.session_manager import SessionManager
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from contracts.interface.Irepositories import IRepositories


class TermsRepository(IRepositories):
    """Data access repository responsible for querying and persisting term entities."""

    def __init__(self, db_session: Session = Depends(SessionManager.get_db)) -> None:
        """Initialize the repository with an active SQLAlchemy database session."""
        self.db = db_session

    async def get_by_id(self, term_id: int) -> Optional[Terms]:
        """Retrieve a term record by its unique UUID identifier."""
        statement = select(Terms).where(Terms.id == term_id)
        return self.db.scalars(statement).first()

    async def get_by_tag_and_version(self, tag: str, version: int) -> Optional[Terms]:
        """Retrieve a term record by its unique tag and version."""
        statement = select(Terms).where((Terms.tag == tag) & (Terms.version == version) & (Terms.active == True))
        return self.db.scalars(statement).first()

    async def create(self, name: str, tag: str, content: str, version: int = 1, active: bool = False) -> Terms:
        """Persist a new term entity in the database and return the refreshed record."""
        term = Terms(name=name, tag=tag, content=content, version=version, active=active)
        try:
            self.db.add(term)
            self.db.commit()
            self.db.refresh(term)
            return term
        except Exception:
            self.db.rollback()
            raise
