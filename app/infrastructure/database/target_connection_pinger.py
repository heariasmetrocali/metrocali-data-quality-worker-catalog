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
# CONTEXTO CENTRALIZADO (Engine factory + Pinger)
# =====================================================================
class TargetConnectionEngineFactory:
    def __init__(self, password_decryptor: PasswordDecryptor) -> None:
        self._password_decryptor = password_decryptor
        self._strategies: dict[ConnectionType, ConnectionStrategy] = {
            ConnectionType.STANDARD: StandardConnectionStrategy(),
            ConnectionType.ORACLE_TNS: OracleTnsConnectionStrategy(),
        }

    def build_engine(self, connection: ConnectionModel) -> Engine:
        password = self._password_decryptor.decrypt(connection.encrypted_password)
        strategy = self._strategies.get(
            connection.connection_type,
            StandardConnectionStrategy(),
        )
        return strategy.create_engine(connection, password)


class TargetConnectionPinger:
    def __init__(
        self,
        password_decryptor: PasswordDecryptor,
        engine_factory: TargetConnectionEngineFactory | None = None,
    ) -> None:
        self._engine_factory = engine_factory or TargetConnectionEngineFactory(
            password_decryptor
        )

    def ping(self, connection: ConnectionModel) -> bool:
        if not connection.enable:
            return False

        engine = self._engine_factory.build_engine(connection)

        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
        finally:
            engine.dispose()