"""Тесты эндпоинтов."""
from fastapi.testclient import TestClient
import pytest
from fastapi import status

from .utils import flip_first_char
from .messages import (
    VALUE_IN_RESPONSE_ERROR, RIGHT_SIGNATURE_ERROR, WRONG_SIGNATURE_ERROR,
    WRONG_MESSAGE_ERROR, EMPTY_MESSAGE_ERROR, LARGE_MESSAGE_ERROR,
    DETERMINISTIC_SIGNATURE, DIFFERENT_MESSAGES, INVALID_CONTENT_TYPE,
    STATUS_CODE, TYPE_OF_VALUE_ERROR, INCORRECT_VALUES, INVALID_SIGNATURE
)


INVALID_MSG_RESPONSE = {'error': 'invalid_msg'}
TOO_LARGE_MSG_RESPONSE = {'error': 'payload_too_large'}


def sign(
    client: TestClient, msg: str,
    expected_status_code: int = status.HTTP_200_OK
) -> dict:
    """Функция шорткат авторизации."""
    body = {
        'msg': msg
    }
    r = client.post('/sign', json=body)
    assert r.status_code == expected_status_code, STATUS_CODE.format(
        body, '/sign', expected_status_code
    )
    return r.json()


def verify(
    client: TestClient, signature: str, msg: str,
    expected_status_code: int = status.HTTP_200_OK
) -> dict:
    """Функция шорткат верификации."""
    body = {
        'msg': msg,
        'signature': signature
    }
    r = client.post('/verify', json=body)
    assert r.status_code == expected_status_code, STATUS_CODE.format(
        body, '/verify', expected_status_code
    )
    return r.json()


@pytest.mark.parametrize(
    'endpoint,required_key,required_type,ans_len',
    [
        ('/sign', 'signature', str, 1),
        ('/verify', 'ok', bool, 1),
    ],
    ids=['sign_contract', 'verify_contract'],
)
def test_response_contracts(client, endpoint, required_key,
                            required_type, ans_len, random_msg):
    """Проверка эндпоинтов /verify и /sign на соблюдение структуры ответа."""
    if endpoint == '/sign':
        data = sign(client, random_msg)
    else:
        sig = sign(client, random_msg)['signature']
        data = verify(client, sig, random_msg)
    assert required_key in data, VALUE_IN_RESPONSE_ERROR.format(required_key)
    assert isinstance(data[required_key], required_type), (
        TYPE_OF_VALUE_ERROR.format(required_key, required_type)
    )
    assert len(data) == ans_len, INCORRECT_VALUES.format(endpoint)


@pytest.mark.parametrize(
    'mutator,expected_ok,message',
    [
        (lambda s: s, True, RIGHT_SIGNATURE_ERROR),
        (flip_first_char, False, WRONG_SIGNATURE_ERROR)
    ],
    ids=['correct_signature', 'incorrect_signature']
)
def test_verify_signature_ok(client, random_msg,
                             mutator, expected_ok, message) -> None:
    """Тест проверки /verify с измененной подписью и без."""
    sign_response = sign(client, random_msg)
    signature = mutator(sign_response['signature'])
    verify_response = verify(client, signature, random_msg)
    assert verify_response == {'ok': expected_ok}, message


@pytest.mark.parametrize(
    'msg',
    [
        (''),
        ('   '),
    ],
    ids=['empty', 'whitespace'])
def test_msg_check_verify_and_sign(client, msg, valid_signature):
    """Проверка валидности msg для /verify и /sign."""
    r = verify(client, valid_signature, msg,
               expected_status_code=status.HTTP_400_BAD_REQUEST)
    assert r == INVALID_MSG_RESPONSE, EMPTY_MESSAGE_ERROR

    r = sign(client, msg, expected_status_code=status.HTTP_400_BAD_REQUEST)
    assert r == INVALID_MSG_RESPONSE, EMPTY_MESSAGE_ERROR


@pytest.mark.parametrize(
    'signature',
    ['@@@', 'YWJj'],
    ids=['invalid_base64url', 'invalid_length'],
)
def test_verify_invalid_signature_format(client, signature, random_msg):
    """Проверка неверных форматов подписи."""
    response = verify(client, signature, random_msg,
                      expected_status_code=status.HTTP_400_BAD_REQUEST)
    assert response == {'error': 'invalid_signature_format'}, (
            INVALID_SIGNATURE)


@pytest.mark.parametrize(
    'mutator,should_be_equal,message',
    [
        (lambda s: s, True, DETERMINISTIC_SIGNATURE),
        (flip_first_char, False, DIFFERENT_MESSAGES)
    ],
    ids=['equal_msg', 'not_equal_msg']
)
def test_sign_signature_logic(client, mutator,
                              should_be_equal, message, random_msg):
    """Тест: устойчивость подписи."""
    msg1 = random_msg
    msg2 = mutator(msg1)
    response1 = sign(client, msg=msg1)
    response2 = sign(client, msg=msg2)
    sig1, sig2 = response1['signature'], response2['signature']
    assert (sig1 == sig2) is should_be_equal, message


def test_sign_large_message(client, large_msg):
    """Тест: слишком большое сообщение → 413."""
    response = sign(client, msg=large_msg,
                    expected_status_code=status.HTTP_413_CONTENT_TOO_LARGE)
    assert response == TOO_LARGE_MSG_RESPONSE, LARGE_MESSAGE_ERROR.format(
        'response', 'error: payload_too_large')


def test_verify_wrong_message(client, random_msg):
    """Тест: верификации разных msg → ok=false."""
    sign_response = sign(client, random_msg)
    signature = sign_response['signature']
    wrong_msg = flip_first_char(random_msg)
    verify_response = verify(client, signature, wrong_msg)
    assert verify_response == {'ok': False}, WRONG_MESSAGE_ERROR


def test_sign_wrong_content_type(client, random_msg):
    """Тест: неверный Content-Type → 422."""
    response = client.post(
        '/sign',
        content=f'msg={random_msg}',
        headers={'Content-Type': 'text/plain'}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT, (
        INVALID_CONTENT_TYPE.format('code', '422')
    )
    assert response.json() == {'error': 'invalid_content_type'}, (
        INVALID_CONTENT_TYPE.format(
            'response', 'error: invalid_content_type'
        )
    )
