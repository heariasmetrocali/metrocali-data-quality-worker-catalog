from abc import ABC, abstractmethod

from app.infrastructure.config.settings import password_plaintext_mode


class PasswordDecryptor(ABC):
    @abstractmethod
    def decrypt(self, encrypted_password: str) -> str:
        pass


class PlaintextPasswordDecryptor(PasswordDecryptor):
    """Dev helper: treats encrypted_password as plain text."""

    def decrypt(self, encrypted_password: str) -> str:
        return encrypted_password


def build_password_decryptor() -> PasswordDecryptor:
    if password_plaintext_mode():
        return PlaintextPasswordDecryptor()
    raise RuntimeError(
        "Encrypted password mode is not implemented yet. "
        "Set PASSWORD_PLAINTEXT_MODE=true for local development."
    )
