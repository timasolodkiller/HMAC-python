"""Все модели приложения."""

from dataclasses import dataclass


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
