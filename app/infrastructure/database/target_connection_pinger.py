import enum
from abc import ABC, abstractmethod
from urllib.parse import quote_plus

from sqlalchemy import Engine, create_engine, text

from app.infrastructure.database.models.connection_model import (
    ConnectionModel,
    ConnectionType
)
from app.infrastructure.security.password_decryptor import PasswordDecryptor


# =====================================================================
# INTERFAZ ABSTRACTA (Strategy)
# =====================================================================
class ConnectionStrategy(ABC):
    """Interfaz base para definir las estrategias de conexión a base de datos."""

    @abstractmethod
    def create_engine(self, connection: ConnectionModel, decrypted_password: str) -> Engine:
        """Extrae los parámetros del JSONB y construye el Engine de SQLAlchemy."""
        pass


# =====================================================================
# IMPLEMENTACIONES CONCRETAS
# =====================================================================
class StandardConnectionStrategy(ConnectionStrategy):
    """Estrategia para conexiones estándar basadas en URI (Host, Puerto, DB)."""

    def create_engine(self, connection: ConnectionModel, decrypted_password: str) -> Engine:
        # Extraemos la metadata de red desde el JSONB (connection_params)
        params = connection.connection_params
        host = params.get("host")
        port = params.get("port")
        database_name = params.get("database_name")

        # Codificación segura de credenciales
        username = quote_plus(connection.username)
        safe_password = quote_plus(decrypted_password)
        driver = connection.driver_name.value  # Extrae el string del Enum

        target_url = f"{driver}://{username}:{safe_password}@{host}:{port}/{database_name}"
        
        return create_engine(target_url, pool_pre_ping=True, future=True)


class OracleTnsConnectionStrategy(ConnectionStrategy):
    """Estrategia avanzada para Oracle utilizando descriptores TNS completos."""

    def create_engine(self, connection: ConnectionModel, decrypted_password: str) -> Engine:
        import oracledb
        
        # Inicializar el cliente grueso de Oracle (indispensable para dar soporte a la 11g)
        try:
            oracledb.init_oracle_client()
        except Exception:
            pass  # Ya se encuentra inicializado en el ciclo de vida de la app

        params = connection.connection_params
        tns_descriptor = params.get("tns_descriptor")

        username = quote_plus(connection.username)
        safe_password = quote_plus(decrypted_password)
        driver = connection.driver_name.value  # Debería retornar "oracle+oracledb"

        # SQLAlchemy permite pasar el descriptor completo TNS justo después del símbolo '@'
        target_url = f"{driver}://{username}:{safe_password}@{tns_descriptor}"
        
        return create_engine(target_url, pool_pre_ping=True, future=True)


# =====================================================================
# CONTEXTO CENTRALIZADO (Pinger + Registry Map)
# =====================================================================
class TargetConnectionPinger:
    def __init__(self, password_decryptor: PasswordDecryptor) -> None:
        self._password_decryptor = password_decryptor
        
        # Centralización de estrategias (Evita el uso de IF/SWITCH)
        # Vinculamos el Enum de la base de datos directamente con su clase ejecutora
        self._strategies: dict[ConnectionType, ConnectionStrategy] = {
            ConnectionType.STANDARD: StandardConnectionStrategy(),
            ConnectionType.ORACLE_TNS: OracleTnsConnectionStrategy(),
        }

    def ping(self, connection: ConnectionModel) -> bool:
        if not connection.enable:
            return False

        # 1. Desencriptar la contraseña en la capa de servicio/aplicación
        password = self._password_decryptor.decrypt(connection.encrypted_password)

        # 2. Resolver la estrategia de forma limpia mediante el mapa (Registry)
        # Si por alguna razón viene un tipo no registrado, cae por defecto a STANDARD
        strategy = self._strategies.get(connection.connection_type, StandardConnectionStrategy())

        # 3. Delegar la creación del motor a la estrategia seleccionada
        engine = strategy.create_engine(connection, password)

        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
        finally:
            # Liberar el pool de conexiones inmediatamente al terminar el testeo
            engine.dispose()