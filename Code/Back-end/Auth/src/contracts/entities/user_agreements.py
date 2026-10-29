"""SQLAlchemy ORM entity mapping for the signup.user_agreements database table."""
import datetime
from typing import Optional
import uuid

from contracts.entities.model import Base
from sqlalchemy import Integer,Boolean, DateTime, String, Text,Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

class UserAgreements(Base):
    """ORM entity representing a registered platform user agreement in the signup.user_agreements table."""

    __tablename__ = "user_agreements"
    __table_args__ = {"schema": "signup"}

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False
    )
    term_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp()
    )
