"""Тест HMACService."""
import hashlib
import hmac
from unittest import mock

import pytest

from .utils import flip_first_char, flip_first_byte
from .messages import (
    INVALID_SIGN, INVALID_SIGN_SIZE, INVALID_SIGN_TYPE,
    INVALID_VERIFY, TIMING_COMPARE, BOOL_RETURN
)


@pytest.mark.parametrize(
    'mutator,should_be_equal',
    [
        (lambda s: s, True),
        (flip_first_char, False),
    ],
    ids=['equal_msgs', 'non_equal_msgs']
)
def test_sign_deterministic(signer, mutator, should_be_equal, random_msg):
    """Тестирование подписи на стабильность и различие для разных сообщений."""
    msg1 = random_msg
    msg2 = mutator(msg1)
    sig1 = signer.sign(msg1)
    sig2 = signer.sign(msg2)
    assert (sig1 == sig2) is should_be_equal, INVALID_SIGN


@pytest.mark.parametrize(
    'mutator_sig, mutator_msg, should_be_verified',
    [
        (lambda s: s, lambda s: s, True),
        (flip_first_byte, lambda s: s, False),
        (lambda s: s, flip_first_char, False)
    ],
    ids=['correct', 'incorrect_sig', 'incorrect_msg']
)
def test_verify_logic(signer, mutator_sig, mutator_msg,
                      should_be_verified, random_msg):
    """Тестирование проверки подписи с измененными сообщением, подписью."""
    sig = signer.sign(random_msg)
    another_sig = mutator_sig(sig)
    new_msg = mutator_msg(random_msg)
    verdict = signer.verify(new_msg, another_sig)
    assert isinstance(verdict, bool), BOOL_RETURN
    assert verdict is should_be_verified, (
        INVALID_VERIFY
    )


@pytest.mark.parametrize(
    'mutator',
    [
        lambda s: '     ',
        lambda s: '',
        lambda s: s
    ],
    ids=['whitespace', 'empty', 'random']
)
def test_sign_returns_sha256_digest_bytes(mutator, signer, random_msg):
    """Тестированеи подписи на валидность размера и типа данных."""
    sig = signer.sign(mutator(random_msg))
    assert isinstance(sig, (bytes, bytearray)), INVALID_SIGN_TYPE
    assert len(sig) == hashlib.sha256().digest_size, INVALID_SIGN_SIZE


def test_verify_uses_compare_digest(signer, random_msg):
    """Тест, что используется тайминг-стойкое сравнение."""
    sig = signer.sign(random_msg)
    with mock.patch('hmac.compare_digest', wraps=hmac.compare_digest) as cd:
        signer.verify(random_msg, sig)
        assert cd.called, TIMING_COMPARE
