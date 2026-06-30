from typing import Any, Dict
import json
from app.domain.repos.broker_consumer_repository import BrokerConsumerPort
import asyncio

import redis.exceptions

class ValkeyConsumerAdapter(BrokerConsumerPort):
    """Adaptador puro de Valkey. Solo extrae datos de la cola."""

    def __init__(self, valkey_client):
        self.client = valkey_client

    async def fetch_next_message(self, queue_name: str) -> Dict[Any, Any] | None:
        try:
            print(f"[ValkeyAdapter][INFO] queue_name: {queue_name}")
            result = await self.client.blpop(queue_name, timeout=20)
            print(f"[ValkeyAdapter][INFO] after blpop - result {result}")
            if result:
                _, raw_message = result
                print(f"[ValkeyAdapter][INFO] catch value: {raw_message}")
                
                return json.loads(raw_message)
                
        except (asyncio.TimeoutError, TimeoutError, redis.exceptions.TimeoutError):
            print ("[ValkeyAdapter] timeout, sleeping..")
            return None

        except Exception as e:
            print(f"[ValkeyAdapter][Error Crítico] Al extraer mensaje: {e}")
            
        return None