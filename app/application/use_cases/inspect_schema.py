from app.domain.entities.catalog_column_entity import CatalogColumn
from app.domain.entities.catalog_table_entity import CatalogTable
from app.domain.repos.catalog_column_repository import CatalogColumnRepository
from app.domain.repos.catalog_table_repository import CatalogTableRepository
from app.domain.repos.schema_inspector import SchemaInspector


class InspectSchemaUseCase:
    def __init__(
        self,
        schema_inspector: SchemaInspector,
        catalog_table_repository: CatalogTableRepository,
        catalog_column_repository: CatalogColumnRepository,
    ) -> None:
        self._schema_inspector = schema_inspector
        self._catalog_table_repository = catalog_table_repository
        self._catalog_column_repository = catalog_column_repository

    def execute(self, catalog_id: str, connection_id: str) -> list[CatalogTable]:
        inspected_tables = self._schema_inspector.inspect(connection_id)
        persisted_tables: list[CatalogTable] = []

        for inspected_table in inspected_tables:
            table = CatalogTable.create(
                catalog_id=catalog_id,
                name=inspected_table.name,
            )
            saved_table = self._catalog_table_repository.save(table)

            for inspected_column in inspected_table.columns:
                column = CatalogColumn.create(
                    table_id=saved_table.id,
                    name=inspected_column.name,
                    data_type=inspected_column.data_type,
                )
                self._catalog_column_repository.save(column)

            persisted_tables.append(saved_table)

        return persisted_tables
