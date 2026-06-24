# MetroCali Data Quality - Worker Catálogo (`worker-catalog`)

## 📋 Descripción General
El `worker-catalog` (Discovery Worker) es un servicio de consola (CLI) distribuido e independiente, desarrollado en Python. Su responsabilidad exclusiva dentro de la arquitectura de Calidad de Datos es conectarse de forma segura y dinámica a las diferentes fuentes de datos origen (*sources*) o destino (*targets*), extraer sus metadatos estructurales (DDL) y registrar una "fotografía" o versión exacta del catálogo actual en la base de datos central de auditoría.

Este componente actúa como la primera fase del pipeline asíncrono de calidad de datos, encargándose de mitigar el acoplamiento ante cambios o extensiones estructurales en el Data Lake o fuentes transaccionales.

---

