from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base
from sqlalchemy import String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.base import Base

class EngineModel(Base):
    __tablename__ = "engines"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    engine_name: Mapped[str] = mapped_column(String(50), nullable=False)  # Ej: 'oracle', 'postgresql'
    version: Mapped[str] = mapped_column(String(20), nullable=False)      # Ej: '11g', '19c'
    driver_name: Mapped[str | None] = mapped_column(String(50), nullable=True) # Permitir nulos según SQL

    # Mapeo de la restricción compuesta UNIQUE (engine_name, version)
    __table_args__ = (
        UniqueConstraint("engine_name", "version", name="unique_engine_version"),
    )