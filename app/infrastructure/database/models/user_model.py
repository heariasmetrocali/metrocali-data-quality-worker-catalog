from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, Enum, func
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.base import Base

import enum

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    AUDITOR = "auditor"
    VIEWER = "viewer"


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )  # Añadido con default del servidor
    
    role: Mapped[RoleEnum] = mapped_column(
        Enum(RoleEnum, values_callable=lambda x: [e.value for e in x]), 
        default=RoleEnum.ADMIN, 
        nullable=False
    )

    enable: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true", nullable=False)  # Añadido