import time

from app.domain.entities.connection_entity import Connection
from app.domain.repos.connection_repository import ConnectionRepository

_HARDCODED_CONNECTIONS: dict[str, dict[str, str | bool]] = {
    "conn-1": {"host": "datalake-source.internal", "reachable": True},
    "conn-2": {"host": "legacy-db.internal", "reachable": False},
}


class FakeConnectionRepository(ConnectionRepository):
    def get_by_id(self, connection_id: str) -> Connection | None:
        time.sleep(0.3)

        data = _HARDCODED_CONNECTIONS.get(connection_id)
        if data is None:
            return None

        return Connection(
            id=connection_id,
            host=str(data["host"]),
            reachable=bool(data["reachable"]),
        )
