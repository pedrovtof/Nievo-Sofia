"""Abstract repository contract enforcing consistent persistence operations."""
from abc import ABC, abstractmethod

class IRepositories(ABC):
    """Interface for repositories to ensure consistent implementation across different data access layers."""

    @abstractmethod
    async def get_by_id(self, entity_id: any):
        """Retrieve an entity by its unique identifier."""
        pass

    @abstractmethod
    async def create(self, **kwargs):
        """Persist a new entity in the database and return the refreshed record."""
        pass
