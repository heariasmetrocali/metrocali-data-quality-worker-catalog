from abc import ABC, abstractmethod

from app.domain.entities.catalog_table_entity import CatalogTable


class CatalogTableRepository(ABC):
    @abstractmethod
    def save(self, table: CatalogTable) -> CatalogTable:
        pass
