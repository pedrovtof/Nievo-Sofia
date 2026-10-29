"""SQLAlchemy ORM entity mapping for the member.device database table."""
import datetime
from typing import Optional
import uuid

from contracts.entities.model import Base
from sqlalchemy import Boolean, DateTime, String, Text,Uuid, func, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

class Device(Base):
    """ORM entity representing a registered device in the member.device table."""

    __tablename__ = "device"
    __table_args__ = {"schema": "member"}

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid.uuid7,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        nullable=False
    )
    x_device_id: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )
    user_agent: Mapped[Optional[str]] = mapped_column(
        String(200),
        nullable=True
    )
    ip_list: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        nullable=True
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
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
