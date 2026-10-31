"""Database engine lifecycle and SQLAlchemy session management utilities."""
from collections.abc import Generator
from typing import Any, Optional

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


class SessionManager:
    """Manages the SQLAlchemy database engine and per-request session lifecycle."""

    _engine: Optional[Engine] = None
    _session_factory: Optional[sessionmaker[Session]] = None

    @classmethod
    def initialize(
        cls,
        db_url: str,
        pool_size: int = 15,
        max_overflow: int = 25,
        **engine_kwargs: Any,
    ) -> None:
        """Initialize the SQLAlchemy engine and session factory if not already configured."""
        if not db_url or not db_url.strip():
            raise ValueError("A valid database connection URL is required to initialize SessionManager.")

        if cls._engine is None:
            options: dict[str, Any] = {
                "pool_pre_ping": True,
                **engine_kwargs,
            }
            if not db_url.startswith("sqlite"):
                options.setdefault("pool_size", pool_size)
                options.setdefault("max_overflow", max_overflow)

            cls._engine = create_engine(db_url, **options)
            cls._session_factory = sessionmaker(
                bind=cls._engine,
                autocommit=False,
                autoflush=False,
                expire_on_commit=False,
            )

    @classmethod
    def get_db(cls) -> Generator[Session, None, None]:
        """Yield a database session for FastAPI dependency injection and ensure cleanup."""
        if cls._session_factory is None:
            raise RuntimeError("Database connection is not initialized. Call SessionManager.initialize() first.")

        db = cls._session_factory()
        try:
            yield db
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    @classmethod
    def get_session(cls) -> Session:
        """Create and return a new database session for standalone or background execution."""
        if cls._session_factory is None:
            raise RuntimeError("SessionManager is not initialized. Call SessionManager.initialize() first.")
        return cls._session_factory()

    @classmethod
    def close(cls) -> None:
        """Dispose the active database engine connection pool and reset manager state."""
        if cls._engine is not None:
            cls._engine.dispose()
            cls._engine = None
        cls._session_factory = None
