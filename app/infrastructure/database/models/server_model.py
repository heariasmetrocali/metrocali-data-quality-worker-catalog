from datetime import datetime
from sqlalchemy import String, Text, DateTime, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.base import Base

class ServerModel(Base):
    __tablename__ = "servers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)  # Corregido longitud y UNIQUE
    ip: Mapped[str] = mapped_column(String(45), nullable=False)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)  # Añadido
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )  # Añadido con default del servidor
    enable: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)  # Añadido