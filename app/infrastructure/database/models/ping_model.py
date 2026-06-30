# app/infrastructure/database/models/ping_log.py
from datetime import datetime
from sqlalchemy import String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.base import Base

class PingLogModel(Base):
    __tablename__ = "ping_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
    )
    
    connection_id: Mapped[int] = mapped_column(
        nullable=False
    )
    
    status: Mapped[str] = mapped_column(
        String(20), 
        server_default="PENDING", 
        nullable=False
    )
    
    comment: Mapped[str | None] = mapped_column(
        Text, 
        nullable=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.timezone('utc', func.now()), 
        nullable=False
    )