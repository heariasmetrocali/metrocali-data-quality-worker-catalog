from uuid import UUID

from app.domain.entities.catalog_column_entity import CatalogColumn
from app.infrastructure.database.models.cat_table_model import CatColumnModel


class CatalogColumnMapper:
    @staticmethod
    def to_domain(model: CatColumnModel) -> CatalogColumn:
        return CatalogColumn(
            id=str(model.id),
            table_id=str(model.table_id),
            name=model.name,
            data_type=model.data_type,
            is_active=model.is_active if model.is_active is not None else True,
        )

    @staticmethod
    def to_model(entity: CatalogColumn) -> CatColumnModel:
        return CatColumnModel(
            id=UUID(entity.id),
            table_id=UUID(entity.table_id),
            name=entity.name,
            data_type=entity.data_type,
            is_active=entity.is_active,
            updated_at=None,
        )
