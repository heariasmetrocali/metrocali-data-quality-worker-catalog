from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.user_entity import User
from app.domain.repos.user_repository import UserRepository
from app.infrastructure.adapters.mappers.user_mapper import to_domain
from app.infrastructure.database.models.user_model import UserModel


class SqlAlchemyUserRepository(UserRepository):
    def __init__(
        self,
        session: Session
    ) -> None:
        self._session = session

    def get_by_id(self, user_id: str) -> User | None:
        try:
            user_pk = int(user_id)
        except ValueError:
            return None

        stmt = (
            select(UserModel)
            .where(UserModel.id == user_pk)
        )

        entity = self._session.scalars(stmt).first()
        if entity is None:
            return None
        
        return to_domain(entity)

