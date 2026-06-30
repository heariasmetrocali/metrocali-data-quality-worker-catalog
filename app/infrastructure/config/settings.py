import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[3]


def load_environment() -> None:
    load_dotenv(PROJECT_ROOT / ".env")
    # load_dotenv(PROJECT_ROOT / ".env.local", override=True)


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class DatabaseSettings:
    url: str | None
    host: str
    port: int
    name: str
    user: str
    password: str
    driver: str

    @classmethod
    def from_env(cls) -> "DatabaseSettings":
        load_environment()
        return cls(
            url=os.getenv("DATABASE_URL"),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            name=os.getenv("DB_NAME", "metrocali_audit"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", ""),
            driver=os.getenv("DB_DRIVER", "postgresql+psycopg"),
        )

    def connection_url(self) -> str:
        if self.url:
            return self.url
        return (
            f"{self.driver}://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.name}"
        )


@lru_cache
def get_database_settings() -> DatabaseSettings:
    return DatabaseSettings.from_env()


@lru_cache
def use_fake_connection_repository() -> bool:
    load_environment()
    return env_flag("USE_FAKE_CONNECTION_REPOSITORY", default=False)


@lru_cache
def password_plaintext_mode() -> bool:
    load_environment()
    return env_flag("PASSWORD_PLAINTEXT_MODE", default=True)
