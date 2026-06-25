from app.domain.entities.user_entity import User
from app.infrastructure.database.models.user_model import UserModel


def to_domain(user: UserModel) -> User:
    return User(
        id=str(user.id),
        name=user.username,
    )
