from abc import ABC, abstractmethod

from app.domain.entities.connection_entity import Connection


class PingRepository(ABC):
    @abstractmethod
    def mark_as_resolved(self, ping_id: int, status: str, comment: str) -> None:
        pass

    @abstractmethod
    def get_by_id (self, ping_id: int) -> dict:
        pass
