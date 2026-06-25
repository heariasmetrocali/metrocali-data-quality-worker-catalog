from sqlalchemy.orm import Session

from app.application.use_cases.create_catalog import CreateCatalogUseCase
from app.domain.repos.connection_repository import ConnectionRepository
from app.infrastructure.adapters.fake_catalog_repository import FakeCatalogRepository
from app.infrastructure.adapters.fake_connection_repository import (
    FakeConnectionRepository,
)
from app.infrastructure.adapters.fake_user_repository import FakeUserRepository
from app.infrastructure.adapters.sqlalchemy_connection_repository import (
    SqlAlchemyConnectionRepository,
)
from app.infrastructure.config.settings import use_fake_connection_repository
from app.infrastructure.database.session import session_scope


def build_connection_repository(session: Session) -> ConnectionRepository:
    if use_fake_connection_repository():
        return FakeConnectionRepository()
    return SqlAlchemyConnectionRepository(session)


def build_create_catalog_use_case(session: Session) -> CreateCatalogUseCase:
    return CreateCatalogUseCase(
        catalog_repository=FakeCatalogRepository(),
        connection_repository=build_connection_repository(session),
        user_repository=FakeUserRepository(),
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
