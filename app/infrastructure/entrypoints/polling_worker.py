import asyncio
from typing import Any, Dict
import redis.asyncio as aioredis

import os

from app.infrastructure.brokers.valkey_consumer import ValkeyConsumerAdapter
from app.infrastructure.composition_root import run_ping_connection_use_case

class PollingEngine:
    """Encargado de manejar el ciclo de vida del loop y el enrutamiento."""
    
    def __init__(self, consumer_port: ValkeyConsumerAdapter, queue_name: str):
        self.consumer = consumer_port
        self.queue_name = queue_name
        self.is_running = True

    async def start_polling(self):
        print(f"[*] Polling Engine iniciado. Escuchando: {self.queue_name}")
        
        while self.is_running:
            try:
                envelope = await self.consumer.fetch_next_message(self.queue_name)
                
                if envelope:
                    asyncio.create_task(self._handle_envelope(envelope))
                    
            except Exception as e:
                print(f"[PollingEngine][Error]: {e}")
                await asyncio.sleep(1)

    async def _handle_envelope(self, envelope: Dict[str, Any]):
        """Handler que extrae y enruta al caso de uso correspondiente."""
        event_type = self._extract_event_type(envelope)
        payload = self._extract_payload(envelope)
        
        print(f"[PollingEngine] Procesando evento tipo: '{event_type}'")
        
        if event_type == "ping":
            ping_id = int(payload.get("ping_id", 0))
            
            print(f"[PollingEngine] Invocando run_ping_connection_use_case para ID: {ping_id}")
            run_ping_connection_use_case(ping_id)
            
        elif event_type == "create-catalog":
            pass
        else:
            print(f"[PollingEngine][Warning] Evento desconocido: {event_type}")

    def _extract_event_type(self, envelope: Dict[str, Any]) -> str:
        return envelope.get("event_type", "unknown")

    def _extract_payload(self, envelope: Dict[str, Any]) -> Dict[str, Any]:
        return envelope.get("payload", {})

    def stop(self):
        self.is_running = False


# --- PUNTO DE ENTRADA PRINCIPAL ---
async def main():
    valkey_url = os.getenv("VALKEY_URL", "redis://localhost:6379")
    queue_name = os.getenv("DATA_QUALITY_QUEUE", "catalog_events_queue")
    
    print(f"[+] Iniciando Worker escuchando la cola: {valkey_url} {queue_name}")

    valkey_client = aioredis.from_url(valkey_url, decode_responses=True)
    
    consumer_adapter = ValkeyConsumerAdapter(valkey_client)
    
    engine = PollingEngine(consumer_port=consumer_adapter, queue_name=queue_name)
    
    try:
        await engine.start_polling()
    except asyncio.CancelledError:
        engine.stop()
        print("[-] Motor de polling detenido de manera controlada.")
    finally:
        await valkey_client.close()

if __name__ == "__main__":
    asyncio.run(main())