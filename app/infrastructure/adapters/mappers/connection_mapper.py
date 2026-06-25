from app.domain.entities.connection_entity import Connection
from app.infrastructure.database.models.connection_model import ConnectionModel


def to_domain(connection: ConnectionModel, reachable: bool) -> Connection:
    return Connection(
        id=str(connection.id),
        reachable=reachable,
    )
