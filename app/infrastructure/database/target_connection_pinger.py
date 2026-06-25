from urllib.parse import quote_plus

from sqlalchemy import create_engine, text

from app.infrastructure.database.models.connection_model import ConnectionModel
from app.infrastructure.security.password_decryptor import PasswordDecryptor


class TargetConnectionPinger:
    def __init__(self, password_decryptor: PasswordDecryptor) -> None:
        self._password_decryptor = password_decryptor

    def ping(self, connection: ConnectionModel) -> bool:
        if not connection.enable:
            return False

        target_url = self._build_target_url(connection)
        engine = create_engine(
            target_url,
            pool_pre_ping=True,
            future=True,
        )

        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception:
            return False
        finally:
            engine.dispose()

    def _build_target_url(self, connection: ConnectionModel) -> str:
        password = self._password_decryptor.decrypt(connection.encrypted_password)
        username = quote_plus(connection.username)
        safe_password = quote_plus(password)
        driver = connection.engine.driver_name
        return (
            f"{driver}://{username}:{safe_password}@"
            f"{connection.host}:{connection.port}/{connection.database_name}"
        )
