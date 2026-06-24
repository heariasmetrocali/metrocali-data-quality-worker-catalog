from abc import ABC, abstractmethod

from app.domain.entities.connection_entity import Connection


class ConnectionRepository(ABC):
    @abstractmethod
    def get_by_id(self, connection_id: str) -> Connection | None:
        pass
