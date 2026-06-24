from app.domain.entities.catalog_aggregate import Catalog
from app.domain.exceptions.catalog_exception import CatalogException
from app.domain.repos.catalog_repository import CatalogRepository
from app.domain.repos.connection_repository import ConnectionRepository
from app.domain.repos.user_repository import UserRepository


class CreateCatalogUseCase:
    def __init__(
        self,
        catalog_repository: CatalogRepository,
        connection_repository: ConnectionRepository,
        user_repository: UserRepository,
    ) -> None:
        self._catalog_repository = catalog_repository
        self._connection_repository = connection_repository
        self._user_repository = user_repository

    def execute(self, connection_id: str, user_id: str, alias: str) -> Catalog:
        user = self._user_repository.get_by_id(user_id)
        if user is None:
            raise CatalogException(f"user '{user_id}' not found")

        connection = self._connection_repository.get_by_id(connection_id)
        if connection is None:
            raise CatalogException(f"connection '{connection_id}' not found")

        catalog = Catalog.create(
            connection_id=connection_id,
            user_id=user_id,
            alias=alias,
        )
        catalog.validate_connection(connection)

        return self._catalog_repository.save(catalog)
