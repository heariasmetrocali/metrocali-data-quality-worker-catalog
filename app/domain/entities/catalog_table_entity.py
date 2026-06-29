from dataclasses import dataclass
from uuid import uuid4

from app.domain.exceptions.catalog_exception import CatalogException


@dataclass
class CatalogTable:
    id: str
    catalog_id: str
    name: str
    is_active: bool = True

    @classmethod
    def create(cls, catalog_id: str, name: str) -> "CatalogTable":
        normalized_name = name.strip()
        if not normalized_name:
            raise CatalogException("table name is mandatory")

        return cls(
            id=str(uuid4()),
            catalog_id=catalog_id,
            name=normalized_name,
            is_active=True,
        )
