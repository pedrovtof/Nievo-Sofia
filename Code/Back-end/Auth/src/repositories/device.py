"""Repository providing persistence operations for the member.device database table."""
from typing import Optional
import uuid

from contracts.entities.device import Device
from core.database.session_manager import SessionManager
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from contracts.interface.Irepositories import IRepositories


class DeviceRepository(IRepositories):
    """Data access repository responsible for querying and persisting Device entities."""

    def __init__(self, db_session: Session = Depends(SessionManager.get_db)) -> None:
        """Initialize the repository with an active SQLAlchemy database session."""
        self.db = db_session

    async def get_by_id(self, device_id: uuid.UUID) -> Optional[Device]:
        """Retrieve a device record by its unique UUID identifier."""
        statement = select(Device).where(Device.id == device_id)
        return self.db.scalars(statement).first()

    async def create_without_commit(self, session: Session,user_id: uuid.UUID, x_device_id: str, ip_list: Optional[list[str]] = None, user_agent: Optional[str] = None) -> Device | bool:
        """Persist a new Device entity in the database without committing the transaction."""
        device = Device(user_id=user_id, x_device_id=x_device_id, ip_list=ip_list, user_agent=user_agent)
        try:
            session.add(device)
            session.flush()
            return device, True
        except Exception as e:
            return str(f"Failed to create device without commit. {e}") , False

    async def create(self, user_id: uuid.UUID, x_device_id: str, ip_list: Optional[list[str]] = None, user_agent: Optional[str] = None) -> Device:
        """Persist a new Device entity in the database and return the refreshed record."""
        device = Device(user_id=user_id, x_device_id=x_device_id, ip_list=ip_list, user_agent=user_agent)
        try:
            self.db.add(device)
            self.db.commit()
            self.db.refresh(device)
            return device
        except Exception:
            self.db.rollback()
            raise