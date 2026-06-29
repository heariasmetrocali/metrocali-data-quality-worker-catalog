

from app.domain.entities.catalog_aggregate import Catalog
from app.domain.repos.connection_repository import ConnectionRepository

class BuildCatalogService:
    def __init__(
        self,
        # cat_table_repository
        # cat_columns reposiotry
        connection_repository: ConnectionRepository
    ) -> None:
        self._connection_repository = connection_repository

    def execute(self, connection_id: Str) -> Catalog:
        print ("...")
        # llamar create_catalog
        # llamar inspect_schema 
        # de los casos de uso.
        # finalmente, persistir en la tabla : cat_tables. por ahora:
