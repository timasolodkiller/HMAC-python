"""Дополнительные полезные функции для тестирования."""


def flip_first_char(sig: str) -> str:
    """Функция дла изменения первого байта текста."""
    return ('A' if sig[0] != 'A' else 'B') + sig[1:]


def flip_first_byte(b: bytes) -> bytes:
    """Функция изменения первого бита."""
    return bytes([b[0] ^ 1]) + b[1:]
