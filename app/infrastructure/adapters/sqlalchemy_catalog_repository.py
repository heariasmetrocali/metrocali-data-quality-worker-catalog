from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.catalog_aggregate import Catalog
from app.domain.repos.catalog_repository import CatalogRepository
from app.infrastructure.adapters.mappers.catalog_mapper import CatalogMapper

class SqlAlchemyCatalogRepository(CatalogRepository):
    def __init__(
        self,
        session: Session
    ) -> None:
        self._session = session

    def save(self, domain: Catalog) -> Catalog | None:
        
        entity = CatalogMapper.to_model(domain)

        self._session.add(entity)
        self._session.flush()
        self._session.commit()

        return CatalogMapper.to_domain(entity)

