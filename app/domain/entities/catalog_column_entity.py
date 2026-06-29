from dataclasses import dataclass
from uuid import uuid4

from app.domain.exceptions.catalog_exception import CatalogException


@dataclass
class CatalogColumn:
    id: str
    table_id: str
    name: str
    data_type: str
    is_active: bool = True

    @classmethod
    def create(cls, table_id: str, name: str, data_type: str) -> "CatalogColumn":
        normalized_name = name.strip()
        normalized_type = data_type.strip()

        if not normalized_name:
            raise CatalogException("column name is mandatory")
        if not normalized_type:
            raise CatalogException("column data_type is mandatory")

        return cls(
            id=str(uuid4()),
            table_id=table_id,
            name=normalized_name,
            data_type=normalized_type,
            is_active=True,
        )
