from dataclasses import dataclass

from app.application.use_cases.create_catalog import CreateCatalogUseCase
from app.application.use_cases.inspect_schema import InspectSchemaUseCase
from app.domain.entities.catalog_aggregate import Catalog
from app.domain.entities.catalog_table_entity import CatalogTable


@dataclass(frozen=True)
class BuildCatalogResult:
    catalog: Catalog
    tables: list[CatalogTable]


class BuildCatalogService:
    def __init__(
        self,
        create_catalog_use_case: CreateCatalogUseCase,
        inspect_schema_use_case: InspectSchemaUseCase,
    ) -> None:
        self._create_catalog = create_catalog_use_case
        self._inspect_schema = inspect_schema_use_case

    def execute(
        self,
        connection_id: str,
        user_id: str,
        alias: str,
    ) -> BuildCatalogResult:
        catalog = self._create_catalog.execute(
            connection_id=connection_id,
            user_id=user_id,
            alias=alias,
        )
        tables = self._inspect_schema.execute(
            catalog_id=catalog.id,
            connection_id=connection_id,
        )
        return BuildCatalogResult(catalog=catalog, tables=tables)
