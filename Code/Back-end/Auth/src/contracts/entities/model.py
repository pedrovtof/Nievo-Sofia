"""Declarative base model configuration for SQLAlchemy ORM entities."""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base declarative class inherited by all SQLAlchemy ORM database entities."""

    pass
