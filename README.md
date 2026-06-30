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




# Metrocali Data Quality - Worker CLI 🚀

Este componente es un script de línea de comandos (CLI) desarrollado en Python 3.12 encargado de ejecutar los procesos pesados de auditoría, procesamiento de calidad de datos e inserción en el esquema `QUALITY_DATA` de Oracle Cloud Infrastructure (OCI ATP), así como la generación de reportes bajo demanda.

Funciona de manera aislada y bajo demanda (Short-lived process) utilizando arquitectura de contenedores con Docker.

---

## 🛠️ Desarrollo Local (Sin Docker)

Si deseas realizar pruebas de laboratorio o desarrollo directo en tu máquina local, sigue estos pasos:

### 1. Preparar el entorno virtual
```bash
# Actualizar pip a la última versión
python -m pip install --upgrade pip

# Instalar las dependencias del proyecto
pip install -r requirements.txt
```


### 2. Ejecutar comandos del CLI
```bash
# El script utiliza un mapa de comandos dinámico. La estructura base de ejecución es:
python main.py [ACTION] [PARAMS]

# Ejemplo: Correr proceso de auditoría (PL/SQL)
python main.py process --schema MERCURY_RAW --table POS_DEVICE
```


### 3. Congelar dependencias (Solo desarrolladores)
```bash
# Si instalas una nueva librería en caliente, recuerda actualizar el archivo de dependencias:
pip freeze > requirements.txt
```



---

## 🐳 Despliegue y Ejecución con Docker (Producción / VM)

Para garantizar la portabilidad de los drivers de Oracle y el aislamiento de recursos en la Máquina Virtual, se debe utilizar Docker.

### 1. Construir la Imagen (Build)
```bash
# Ejecuta el siguiente comando en la raíz donde se encuentra el 'Dockerfile.worker':
docker build -t metrocali-data-quality-worker:0.1.0-alpha.1 .
```


### 2. Ejecutar el Proceso de Auditoría (process)
```bash
# Este comando levantará un contenedor temporal, inyectará las variables de entorno, ejecutará el procedimiento en la base de datos autónoma de OCI y destruirá el contenedor al terminar para liberar RAM/CPU.
docker run --rm  --env-file .env.worker metrocali-data-quality-worker:0.1.0-alpha.1 process --schema MERCURY_RAW --table APPLICATIONS
```


---

## ⚙️ Variables de Entorno Requeridas (.env.worker)

El archivo de configuración ambiental debe contener las credenciales de acceso seguro a OCI ATP:

```bash
OCI_ATP_USER=QUALITY_DATA

```




