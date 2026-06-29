from sqlalchemy.orm import Session

from app.application.use_cases.create_catalog import CreateCatalogUseCase
from app.infrastructure.adapters.sqlalchemy_catalog_repository import SqlAlchemyCatalogRepository
from app.infrastructure.adapters.sqlalchemy_connection_repository import (
    SqlAlchemyConnectionRepository,
)

from app.infrastructure.adapters.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.infrastructure.database.session import session_scope

def build_create_catalog_use_case(session: Session) -> CreateCatalogUseCase:
    return CreateCatalogUseCase(
        catalog_repository=SqlAlchemyCatalogRepository(session),
        connection_repository=SqlAlchemyConnectionRepository(session),
        user_repository=SqlAlchemyUserRepository(session),
    )

def run_create_catalog_use_case(
    connection_id: str,
    user_id: str,
    alias: str,
):
    with session_scope() as session:
        use_case = build_create_catalog_use_case(session)
        return use_case.execute(
            connection_id=connection_id,
            user_id=user_id,
            alias=alias,
        )
