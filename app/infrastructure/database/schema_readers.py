from abc import ABC, abstractmethod

from sqlalchemy import Engine, text

from app.domain.value_objects.schema_inspection import InspectedColumn, InspectedTable
from app.infrastructure.database.models.connection_model import ConnectionModel


class SchemaReaderStrategy(ABC):
    @abstractmethod
    def read(self, engine: Engine, connection: ConnectionModel) -> list[InspectedTable]:
        pass


class PostgresSchemaReader(SchemaReaderStrategy):
    def read(self, engine: Engine, connection: ConnectionModel) -> list[InspectedTable]:
        schema_name = connection.connection_params.get("schema", "data_quality")

        tables_query = text(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = :schema_name
              AND table_type = 'BASE TABLE'
            ORDER BY table_name
            """
        )
        columns_query = text(
            """
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = :schema_name
              AND table_name = :table_name
            ORDER BY ordinal_position
            """
        )

        inspected_tables: list[InspectedTable] = []

        with engine.connect() as conn:
            table_rows = conn.execute(
                tables_query,
                {"schema_name": schema_name},
            ).fetchall()

            for (table_name,) in table_rows:
                column_rows = conn.execute(
                    columns_query,
                    {"schema_name": schema_name, "table_name": table_name},
                ).fetchall()
                columns = [
                    InspectedColumn(name=column_name, data_type=data_type)
                    for column_name, data_type in column_rows
                ]
                inspected_tables.append(
                    InspectedTable(name=table_name, columns=columns)
                )

        return inspected_tables


class OracleSchemaReader(SchemaReaderStrategy):
    def read(self, engine: Engine, connection: ConnectionModel) -> list[InspectedTable]:
        schema_name = connection.connection_params.get(
            "schema",
            connection.username.upper(),
        )

        tables_query = text(
            """
            SELECT table_name
            FROM all_tables
            WHERE owner = :schema_name
            ORDER BY table_name
            """
        )
        columns_query = text(
            """
            SELECT column_name, data_type
            FROM all_tab_columns
            WHERE owner = :schema_name
              AND table_name = :table_name
            ORDER BY column_id
            """
        )

        inspected_tables: list[InspectedTable] = []

        with engine.connect() as conn:
            table_rows = conn.execute(
                tables_query,
                {"schema_name": schema_name.upper()},
            ).fetchall()

            for (table_name,) in table_rows:
                column_rows = conn.execute(
                    columns_query,
                    {
                        "schema_name": schema_name.upper(),
                        "table_name": table_name,
                    },
                ).fetchall()
                columns = [
                    InspectedColumn(name=column_name, data_type=data_type)
                    for column_name, data_type in column_rows
                ]
                inspected_tables.append(
                    InspectedTable(name=table_name, columns=columns)
                )

        return inspected_tables
