import time

from app.domain.entities.catalog_aggregate import Catalog
from app.domain.repos.catalog_repository import CatalogRepository


class FakeCatalogRepository(CatalogRepository):
    def __init__(self) -> None:
        self._storage: dict[str, Catalog] = {}

    def save(self, catalog: Catalog) -> Catalog:
        time.sleep(0.4)
        self._storage[catalog.id] = catalog
        return catalog
