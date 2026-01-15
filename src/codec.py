"""Модуль для кодирования и декодирования base64url."""

import base64
import re


SIGNATURE_BYTES_LENGTH = 32


def encode_signature(sig_bytes: bytes) -> str:
    """Кодирует байты подписи в строку base64url без паддинга."""
    return base64.urlsafe_b64encode(sig_bytes).rstrip(b'=').decode('ascii')


def decode_signature(sig_str: str) -> bytes:
    """Декодирует строку base64url обратно в байты."""
    pad = (-len(sig_str)) % 4
    sig_str += '=' * pad
    return base64.urlsafe_b64decode(sig_str)


def is_valid_base64url(sig_str: str) -> bool:
    """Проверяет, является ли строка валидным base64url форматом."""
    if not isinstance(sig_str, str) or sig_str == '':
        return False

    if not re.match(r'^[A-Za-z0-9_-]+$', sig_str):
        return False

    try:
        decoded = decode_signature(sig_str)
        if len(decoded) != SIGNATURE_BYTES_LENGTH:
            return False
    except Exception:
        return False

    return True
