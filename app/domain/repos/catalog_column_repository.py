from abc import ABC, abstractmethod

from app.domain.entities.catalog_column_entity import CatalogColumn


class CatalogColumnRepository(ABC):
    @abstractmethod
    def save(self, column: CatalogColumn) -> CatalogColumn:
        pass
