import enum
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, Enum, func
from sqlalchemy.dialects.postgresql import JSONB  # Forzamos el uso de JSONB binario en Postgres
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.database.models.server_model import ServerModel


class DatabaseEngine(str, enum.Enum):
    ORACLE = "ORACLE"
    POSTGRESQL = "POSTGRESQL"


class ConnectionType(str, enum.Enum):
    STANDARD = "STANDARD"
    ORACLE_TNS = "ORACLE_TNS"


class DriverName(str, enum.Enum):
    POSTGRES_SQL = "postgresql+psycopg"
    ORACLE_DB = "oracle+oracledb"


class ConnectionModel(Base):
    __tablename__ = "connections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    
    # Llave foránea hacia Servidores (Se mantiene)
    server_id: Mapped[int] = mapped_column(
        ForeignKey("servers.id", ondelete="RESTRICT"),
        nullable=False,
    )
    
    # Nuevas Columnas de Control basadas en Enums
    engine: Mapped[DatabaseEngine] = mapped_column(
        Enum(DatabaseEngine), 
        nullable=False
    )
    connection_type: Mapped[ConnectionType] = mapped_column(
        Enum(ConnectionType), 
        default=ConnectionType.STANDARD, 
        nullable=False
    )

    driver_name: Mapped[DriverName] = mapped_column(
        Enum(DriverName, values_callable=lambda x: [e.value for e in x]), 
        nullable=False
    )

    # Credenciales Fijas (Fuera del JSON por diseño de seguridad y criptografía)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    encrypted_password: Mapped[str] = mapped_column(Text, nullable=False)

    # El contenedor dinámico y óptimo que absorbe host, port, tns_descriptor, etc.
    connection_params: Mapped[dict] = mapped_column(
        JSONB, 
        default=dict, 
        nullable=False
    )

    # Campos de Auditoría (Se mantienen consistentes con tu base original)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    enable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relaciones de ORM
    server: Mapped["ServerModel"] = relationship()