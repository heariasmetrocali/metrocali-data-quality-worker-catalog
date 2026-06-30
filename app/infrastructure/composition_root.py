from sqlalchemy.orm import Session

from app.application.services.build_catalog import BuildCatalogResult, BuildCatalogService

from app.application.use_cases.create_catalog import CreateCatalogUseCase
from app.application.use_cases.inspect_schema import InspectSchemaUseCase
from app.application.use_cases.ping_connection import PingConnectionUseCase

from app.infrastructure.adapters.sqlalchemy_catalog_column_repository import (
    SqlAlchemyCatalogColumnRepository,
)
from app.infrastructure.adapters.sqlalchemy_catalog_repository import (
    SqlAlchemyCatalogRepository,
)
from app.infrastructure.adapters.sqlalchemy_catalog_table_repository import (
    SqlAlchemyCatalogTableRepository,
)
from app.infrastructure.adapters.sqlalchemy_connection_repository import (
    SqlAlchemyConnectionRepository,
)

from app.infrastructure.adapters.sqlalchemy_ping_repository import (
    SqlAlchemyPingRepository,
)

from app.infrastructure.adapters.sqlalchemy_schema_inspector import (
    SqlAlchemySchemaInspector,
)
from app.infrastructure.adapters.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.infrastructure.database.session import session_scope


def build_build_catalog_service(session: Session) -> BuildCatalogService:
    create_catalog_use_case = CreateCatalogUseCase(
        catalog_repository=SqlAlchemyCatalogRepository(session),
        connection_repository=SqlAlchemyConnectionRepository(session),
        user_repository=SqlAlchemyUserRepository(session),
    )
    inspect_schema_use_case = InspectSchemaUseCase(
        schema_inspector=SqlAlchemySchemaInspector(session),
        catalog_table_repository=SqlAlchemyCatalogTableRepository(session),
        catalog_column_repository=SqlAlchemyCatalogColumnRepository(session),
    )
    return BuildCatalogService(
        create_catalog_use_case=create_catalog_use_case,
        inspect_schema_use_case=inspect_schema_use_case,
    )


def run_build_catalog_service(
    connection_id: str,
    user_id: str,
    alias: str,
) -> BuildCatalogResult:
    with session_scope() as session:
        service = build_build_catalog_service(session)
        result = service.execute(
            connection_id=connection_id,
            user_id=user_id,
            alias=alias,
        )
        session.commit()
        return result


def run_ping_connection_use_case(
    ping_id: int
) -> None:
    with session_scope() as session:
        use_case = PingConnectionUseCase(
            ping_repository=SqlAlchemyPingRepository(session),
            connection_repository=SqlAlchemyConnectionRepository(session)
        )

        use_case.execute(ping_id)
        session.commit()
        print ("[ROOT] executed use case - ping connection..")
