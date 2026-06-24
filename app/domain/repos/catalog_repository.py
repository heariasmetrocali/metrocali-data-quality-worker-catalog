from abc import ABC, abstractmethod

from app.domain.entities.catalog_aggregate import Catalog


class CatalogRepository(ABC):
    @abstractmethod
    def save(self, catalog: Catalog) -> Catalog:
        pass
