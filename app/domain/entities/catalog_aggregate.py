from dataclasses import dataclass
from uuid import uuid4

from app.domain.entities.connection_entity import Connection
from app.domain.exceptions.catalog_exception import CatalogException


@dataclass
class Catalog:
    id: str
    alias: str
    connection_id: str
    user_id: str

    @classmethod
    def create(cls, connection_id: str, user_id: str, alias: str) -> "Catalog":
        catalog = cls(
            id=str(uuid4()),
            alias=alias,
            connection_id=connection_id,
            user_id=user_id,
        )
        catalog.check_catalog()
        return catalog

    def check_catalog(self) -> None:
        if not self.alias or not self.alias.strip():
            raise CatalogException("alias is mandatory")

    def validate_connection(self, connection: Connection) -> None:
        if not connection.ping():
            raise CatalogException(
                f"connection '{connection.id}' is not reachable"
            )
