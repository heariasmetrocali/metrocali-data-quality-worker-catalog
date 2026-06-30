from abc import ABC, abstractmethod
from typing import Any, Dict

class BrokerConsumerPort(ABC):
    """Puerto de entrada/salida para consumir mensajes de forma agnóstica."""

    @abstractmethod
    async def fetch_next_message(self, queue_name: str) -> Dict[str, Any] | None:
        """Obtiene el siguiente mensaje crudo de la cola sin procesar."""
        pass