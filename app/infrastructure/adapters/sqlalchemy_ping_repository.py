from sqlalchemy.orm import Session
from sqlalchemy import select

from app.domain.repos.ping_repository import PingRepository
from app.infrastructure.database.models.ping_model import PingLogModel

class SqlAlchemyPingRepository(PingRepository):
    """Implementación concreta del repositorio usando SQLAlchemy."""
    
    def __init__(self, session: Session):
        self.session = session

    def mark_as_resolved(self, ping_id: int, status: str, comment: str) -> None:
        """Busca el registro por ID y actualiza su estado y comentario."""
        stmt = select(PingLogModel).where(PingLogModel.id == ping_id)
        db_ping = self.session.execute(stmt).scalar_one_or_none()
        
        if db_ping:
            db_ping.status = status
            db_ping.comment = comment
            
            self.session.commit()
            print(f"[Repository] Ping {ping_id} marcado como {status}")
        else:
            print(f"[Repository][Warning] No se encontró el ping_log con ID {ping_id}")

    def get_by_id(self, ping_id: int) -> dict:
        """Busca un ping por ID y lo retorna mapeado como un diccionario plano."""
        stmt = select(PingLogModel).where(PingLogModel.id == ping_id)
        db_ping = self.session.execute(stmt).scalar_one_or_none()
        
        if not db_ping:
            return {}
            
        return {
            "id": db_ping.id,
            "connection_id": db_ping.connection_id,
            "status": db_ping.status,
            "comment": db_ping.comment,
            "created_at": db_ping.created_at.isoformat() if db_ping.created_at else None
        }