from uuid import UUID

from app.domain.entities.catalog_table_entity import CatalogTable
from app.infrastructure.database.models.cat_table_model import CatTableModel


class CatalogTableMapper:
    @staticmethod
    def to_domain(model: CatTableModel) -> CatalogTable:
        return CatalogTable(
            id=str(model.id),
            catalog_id=str(model.catalog_id),
            name=model.name,
            is_active=model.is_active if model.is_active is not None else True,
        )

    @staticmethod
    def to_model(entity: CatalogTable) -> CatTableModel:
        return CatTableModel(
            id=UUID(entity.id),
            catalog_id=UUID(entity.catalog_id),
            name=entity.name,
            is_active=entity.is_active,
            updated_at=None,
        )
