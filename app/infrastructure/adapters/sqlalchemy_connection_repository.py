from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.domain.entities.connection_entity import Connection
from app.domain.repos.connection_repository import ConnectionRepository
from app.infrastructure.adapters.mappers.connection_mapper import to_domain
from app.infrastructure.database.models.connection_model import ConnectionModel
from app.infrastructure.database.target_connection_pinger import TargetConnectionPinger
from app.infrastructure.security.password_decryptor import (
    PasswordDecryptor,
    build_password_decryptor,
)


class SqlAlchemyConnectionRepository(ConnectionRepository):
    def __init__(
        self,
        session: Session,
        pinger: TargetConnectionPinger | None = None,
        password_decryptor: PasswordDecryptor | None = None,
    ) -> None:
        self._session = session
        decryptor = password_decryptor or build_password_decryptor()
        self._pinger = pinger or TargetConnectionPinger(decryptor)

    def get_by_id(self, connection_id: str) -> Connection | None:
        try:
            connection_pk = int(connection_id)
        except ValueError:
            return None

        stmt = (
            select(ConnectionModel)
            .options(
                joinedload(ConnectionModel.engine),
                joinedload(ConnectionModel.server),
            )
            .where(ConnectionModel.id == connection_pk)
        )
        connection = self._session.scalars(stmt).first()
        if connection is None:
            return None

        reachable = self._pinger.ping(connection)
        return to_domain(connection, reachable)
