"""SQLAlchemy ORM entity mapping for the signup.terms database table."""
import datetime
from typing import Optional
import uuid

from contracts.entities.model import Base
from sqlalchemy import Integer,Boolean, DateTime, String, Text,Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

class Terms(Base):
    """ORM entity representing a registered term in the signup.terms table."""

    __tablename__ = "terms"
    __table_args__ = {"schema": "signup"}

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    name: Mapped[Optional[str]] = mapped_column(
        String(150),
        nullable=False
    )
    tag: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=False
    )
    content: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=False
    )
    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )
