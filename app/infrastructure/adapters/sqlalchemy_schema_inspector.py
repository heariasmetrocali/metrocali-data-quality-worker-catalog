from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.exceptions.catalog_exception import CatalogException
from app.domain.repos.schema_inspector import SchemaInspector
from app.domain.value_objects.schema_inspection import InspectedTable
from app.infrastructure.database.models.connection_model import (
    ConnectionModel,
    DatabaseEngine,
)
from app.infrastructure.database.schema_readers import (
    OracleSchemaReader,
    PostgresSchemaReader,
)
from app.infrastructure.database.target_connection_pinger import (
    TargetConnectionEngineFactory,
    TargetConnectionPinger,
)
from app.infrastructure.security.password_decryptor import (
    PasswordDecryptor,
    build_password_decryptor,
)


class SqlAlchemySchemaInspector(SchemaInspector):
    def __init__(
        self,
        session: Session,
        engine_factory: TargetConnectionEngineFactory | None = None,
        pinger: TargetConnectionPinger | None = None,
        password_decryptor: PasswordDecryptor | None = None,
    ) -> None:
        self._session = session
        decryptor = password_decryptor or build_password_decryptor()
        self._engine_factory = engine_factory or TargetConnectionEngineFactory(
            decryptor
        )
        self._pinger = pinger or TargetConnectionPinger(
            decryptor,
            engine_factory=self._engine_factory,
        )
        self._readers = {
            DatabaseEngine.POSTGRESQL: PostgresSchemaReader(),
            DatabaseEngine.ORACLE: OracleSchemaReader(),
        }

    def inspect(self, connection_id: str) -> list[InspectedTable]:
        connection = self._load_connection(connection_id)
        if connection is None:
            raise CatalogException(f"connection '{connection_id}' not found")

        if not self._pinger.ping(connection):
            raise CatalogException(
                f"connection '{connection_id}' is not reachable for schema inspection"
            )

        engine = self._engine_factory.build_engine(connection)
        reader = self._readers.get(connection.engine)
        if reader is None:
            raise CatalogException(
                f"unsupported database engine '{connection.engine}'"
            )

        try:
            return reader.read(engine, connection)
        finally:
            engine.dispose()

    def _load_connection(self, connection_id: str) -> ConnectionModel | None:
        try:
            connection_pk = int(connection_id)
        except ValueError:
            return None

        stmt = select(ConnectionModel).where(ConnectionModel.id == connection_pk)
        return self._session.scalars(stmt).first()
