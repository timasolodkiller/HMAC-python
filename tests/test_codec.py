"""Тест codec."""
import pytest

from src.codec import (
    encode_signature, decode_signature,
    SIGNATURE_BYTES_LENGTH, is_valid_base64url
)
from .messages import ROUND_TRIP_ERROR, VALID_BASE64URL, DECODE_LENGTH_ERROR


def test_round_trip(raw_sig):
    """Проверка, что кодирование и декодирование взаимно-однозначны."""
    s = encode_signature(raw_sig)
    out = decode_signature(s)
    assert len(out) == SIGNATURE_BYTES_LENGTH, DECODE_LENGTH_ERROR
    assert raw_sig == out, ROUND_TRIP_ERROR


@pytest.mark.parametrize(
    'sig',
    [
        '', None, 123, 'YYYY',
        '@@@', 'abc$', 'a b', 'a=', '////', '+++',
    ],
    ids=[
        'empty', 'none', 'not_str', 'wrong_length',
        'at', 'dollar', 'space', 'equals', 'slashes', 'pluses',
    ],
)
def test_is_valid_base64url_returns_false_for_invalid_inputs(sig):
    """Проверка, что codec не принимает неверные входы."""
    assert is_valid_base64url(sig) is False, VALID_BASE64URL


def test_is_valid_base64url_true_for_encoded_signature(raw_sig):
    """Проверка, что на корректном наборе байт все будет окей."""
    s = encode_signature(raw_sig)
    assert is_valid_base64url(s) is True, VALID_BASE64URL
