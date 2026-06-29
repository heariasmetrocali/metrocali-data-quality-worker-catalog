from sqlalchemy.orm import Session

from app.domain.entities.catalog_table_entity import CatalogTable
from app.domain.repos.catalog_table_repository import CatalogTableRepository
from app.infrastructure.adapters.mappers.catalog_table_mapper import CatalogTableMapper


class SqlAlchemyCatalogTableRepository(CatalogTableRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, table: CatalogTable) -> CatalogTable:
        model = CatalogTableMapper.to_model(table)
        self._session.add(model)
        self._session.flush()
        return CatalogTableMapper.to_domain(model)
