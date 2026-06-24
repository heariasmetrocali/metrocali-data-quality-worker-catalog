from abc import ABC, abstractmethod

from app.domain.entities.user_entity import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: str) -> User | None:
        pass
