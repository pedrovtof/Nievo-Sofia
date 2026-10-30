"""SQLAlchemy ORM entity mapping for the member.user database table."""
import datetime
from typing import Optional
import uuid

from contracts.entities.model import Base
from sqlalchemy import Boolean, DateTime, String, Text,Uuid, func
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    """ORM entity representing a registered platform user in the member.user table."""

    __tablename__ = "user"
    __table_args__ = {"schema": "member"}

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid7,
    )
    full_name: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True,
        default=None,
    )
    nick_name: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=True,
        default=None,
    )
    email: Mapped[Optional[str]] = mapped_column(
        String(150),
        unique=True,
        nullable=True,
        default=None,
    )
    phone: Mapped[Optional[str]] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
        default=None,
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    password: Mapped[str] = mapped_column(
        Text,
        unique=False,
        nullable=False,
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def __repr__(self) -> str:
        """Return a readable string representation of the User entity."""
        return f"<User(id={self.id}, email={self.email}, active={self.active})>"
