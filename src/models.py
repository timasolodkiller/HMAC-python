"""Все модели приложения."""
import base64

from dataclasses import dataclass

from .exceptions.exceptions import ConfigError


@dataclass(frozen=True)
class SignRequest:
    """Модель для /sign запроса."""

    msg: str


@dataclass(frozen=True)
class VerifyRequest:
    """Модель для /verify запроса."""

    msg: str
    signature: str


@dataclass(frozen=True)
class VerifyResponse:
    """Модель для /verify ответа."""

    ok: bool


@dataclass(frozen=True)
class Settings:
    """Модель для config."""

    host: str
    port: int
    max_msg_size_bytes: int
    secret: str
    hmac_alg: str
    log_level: str
    listen: str

    def __post_init__(self):
        """Функция проверки секрета."""
        try:
            base64.b64decode(self.secret, validate=True)
        except Exception as e:
            raise ConfigError('invalid_secret') from e
