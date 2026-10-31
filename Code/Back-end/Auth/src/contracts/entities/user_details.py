"""SQLAlchemy ORM entity mapping for the member.user_details database table."""
import datetime
from typing import Optional
import uuid

from contracts.entities.model import Base
from sqlalchemy import Integer,Boolean, DateTime, String, Text,Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

class UserDetails(Base):
    """ORM entity representing member personal profile details in the member.user_details table."""

    __tablename__ = "user_details"
    __table_args__ = {"schema": "member"}

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid7,
    )
    born_date: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp()
    )
    country_id: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )
    validated_email: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    validated_phone: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )
    address: Mapped[str] = mapped_column(
        String(150),
        nullable=True
    )
    document: Mapped[str] = mapped_column(
        String(150),
        nullable=True
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.current_timestamp()
    )
