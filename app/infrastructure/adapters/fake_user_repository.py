import time

from app.domain.entities.user_entity import User
from app.domain.repos.user_repository import UserRepository

_HARDCODED_USERS: dict[str, str] = {
    "user-1": "Ana Operadora",
    "user-2": "Carlos Auditor",
}


class FakeUserRepository(UserRepository):
    def get_by_id(self, user_id: str) -> User | None:
        time.sleep(0.2)

        name = _HARDCODED_USERS.get(user_id)
        if name is None:
            return None

        return User(id=user_id, name=name)
