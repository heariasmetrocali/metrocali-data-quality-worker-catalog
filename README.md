# MetroCali Data Quality - Worker Catálogo (`worker-catalog`)

## 📋 Descripción General
El `worker-catalog` (Discovery Worker) es un servicio de consola (CLI) distribuido e independiente, desarrollado en Python. Su responsabilidad exclusiva dentro de la arquitectura de Calidad de Datos es conectarse de forma segura y dinámica a las diferentes fuentes de datos origen (*sources*) o destino (*targets*), extraer sus metadatos estructurales (DDL) y registrar una "fotografía" o versión exacta del catálogo actual en la base de datos central de auditoría.

Este componente actúa como la primera fase del pipeline asíncrono de calidad de datos, encargándose de mitigar el acoplamiento ante cambios o extensiones estructurales en el Data Lake o fuentes transaccionales.

---

python -m app create-catalog --connection-id conn-1 --user-id user-1 --alias "Catalogo Produccion"



pip install sqlalchemy python-dotenv psycopg[binary]



comando para instalar 

python -m app.infrastructure.entrypoints.polling_worker

comando para testear el broker.

docker exec -it local_valkey sh

valkey-cli

LPUSH catalog_events_queue '{"event_type":"ping","payload":{"ping_id":1}}'

LRANGE catalog_events_queue 0 -1
