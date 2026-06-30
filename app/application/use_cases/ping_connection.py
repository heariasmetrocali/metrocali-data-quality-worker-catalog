from app.domain.exceptions.catalog_exception import CatalogException
from app.domain.repos.connection_repository import ConnectionRepository
from app.domain.repos.ping_repository import PingRepository


class PingConnectionUseCase:
    def __init__(
        self,
        ping_repository: PingRepository,
        connection_repository: ConnectionRepository
    ) -> None:
        self._ping_repository = ping_repository
        self._connection_repository = connection_repository

    def execute(self, ping_id: int) -> None:
        entity = self._ping_repository.get_by_id(ping_id)
        if not entity:
            raise CatalogException(f"Ping '{ping_id}' not found")

        connection_id = entity.get("connection_id") if isinstance(entity, dict) else getattr(entity, "connection_id", None)
        print(f"[UseCase] Connection_id extraído: {connection_id}")

        try:
            connection = self._connection_repository.get_by_id(connection_id)
            if not connection:
                raise CatalogException(f"Connection metadata for ID '{connection_id}' not found")

            if connection.ping():
                status = "SUCCESS"
                comment = "Conexión establecida y validada correctamente de forma asíncrona."
            else:
                status = "FAILED"
                comment = "No se pudo establecer respuesta del servidor destino (Timeout/Rechazado)."

            self._ping_repository.mark_as_resolved(
                ping_id=ping_id,
                status=status,
                comment=comment
            )
            print(f"[UseCase] Ping {ping_id} marcado como {status}")

        except Exception as e:
            error_msg = f"Error crítico procesando el ping: {str(e)}"
            print(f"[UseCase][Error] {error_msg}")
            self._ping_repository.mark_as_resolved(
                ping_id=ping_id,
                status="ERROR",
                comment=error_msg[:500]
            )
