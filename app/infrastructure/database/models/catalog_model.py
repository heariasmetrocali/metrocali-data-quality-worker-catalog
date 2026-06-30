from datetime import datetime
from uuid import UUID
from sqlalchemy import String, DateTime, text, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.base import Base

class CatalogModel(Base):
    __tablename__ = "catalog"
    __table_args__ = {"schema": "data_quality"}

    # Recibe el UUID generado por el dominio. No usamos server_default aquí.
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        primary_key=True
    )
    
    # Tu DDL especifica int4 para connection_id. 
    # Si en tu dataclass usas str, el mapper hará la conversión a int.
    connection_id: Mapped[int] = mapped_column(Integer, nullable=False)
    catalog_alias: Mapped[str] = mapped_column(String(100), nullable=False)
    user_id: Mapped[str] = mapped_column(String(50), nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=text("CURRENT_TIMESTAMP"), 
        nullable=True
    )