from sqlalchemy.orm import Session

from app.domain.entities.catalog_column_entity import CatalogColumn
from app.domain.repos.catalog_column_repository import CatalogColumnRepository
from app.infrastructure.adapters.mappers.catalog_column_mapper import CatalogColumnMapper


class SqlAlchemyCatalogColumnRepository(CatalogColumnRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def save(self, column: CatalogColumn) -> CatalogColumn:
        model = CatalogColumnMapper.to_model(column)
        self._session.add(model)
        self._session.flush()
        return CatalogColumnMapper.to_domain(model)
