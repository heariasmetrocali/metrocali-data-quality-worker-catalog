from uuid import UUID
from app.domain.entities.catalog_aggregate import Catalog
from app.infrastructure.database.models.catalog_model import CatalogModel

class CatalogMapper:
    @staticmethod
    def to_domain(model: CatalogModel) -> Catalog:
        if not model:
            return None
        return Catalog(
            id=str(model.id),
            alias=model.catalog_alias,
            connection_id=str(model.connection_id), # Mapeado a string como tu dataclass
            user_id=model.user_id
            # Nota: Si necesitas el created_at en el dominio a futuro, 
            # podrías agregarlo como un campo opcional en tu dataclass.
        )

    @staticmethod
    def to_model(entity: Catalog) -> CatalogModel:
        if not entity:
            return None
        
        return CatalogModel(
            id=UUID(entity.id),
            catalog_alias=entity.alias,
            connection_id=int(entity.connection_id), # Conversión estricta al int4 del DDL
            user_id=entity.user_id,
            created_at=None # Permite que la DB asigne el CURRENT_TIMESTAMP por defecto al insertar
        )