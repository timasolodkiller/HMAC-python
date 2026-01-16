"""Подготовка данных фикстурами."""
import json
import base64
import random
import string

import pytest
from fastapi.testclient import TestClient

from src.app import app
from src.utils import get_config_path
from src.hmac_service import HMACSigner

RAW_SECRET = b'unit-test-secret-key-123'
K = 10


@pytest.fixture(scope='session')
def client():
    """Фикстура тестового клиента."""
    return TestClient(app)


@pytest.fixture(scope='session')
def valid_signature(client) -> str:
    """Фикстура валидной подписи."""
    r = client.post('/sign', json={'msg': 'ping'})
    assert r.status_code == 200
    data = r.json()
    assert 'signature' in data
    return data['signature']


@pytest.fixture(scope='session')
def raw_config() -> dict:
    """Фикстура загрузки конфига."""
    config_path = get_config_path(__file__)
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


@pytest.fixture(scope='session')
def max_msg_size(raw_config: dict) -> int:
    """Фикстура извлечения максимального размера сообщения."""
    return int(raw_config['max_msg_size_bytes'])


@pytest.fixture(scope='session')
def large_msg(max_msg_size: int) -> str:
    """Фикстура создания сообщения, превышающего по размеру максимальный."""
    return 'A' * (max_msg_size + 1)


@pytest.fixture(scope='session')
def secret_key_b64() -> str:
    """Фикстура создания секретного ключа."""
    return base64.b64encode(RAW_SECRET).decode('ascii')


@pytest.fixture(scope='session')
def signer(secret_key_b64: str) -> HMACSigner:
    """Фикстура создания объекта класса HMACSigner."""
    return HMACSigner(secret_key_b64)


@pytest.fixture(scope='function')
def random_msg() -> str:
    """Фикстура создания рандомного сообщения."""
    return ''.join(random.choices(string.ascii_letters, k=K))


@pytest.fixture
def raw_sig() -> bytes:
    """Фикстура создания 32 байтов."""
    return bytes(range(32))


@pytest.fixture
def valid_config_dict() -> dict:
    """Валидный конфиг."""
    return {
        'host': '0.0.0.0',
        'port': 8080,
        'max_msg_size_bytes': 1048576,
        'secret': 'c2VjcmV0',
        'hmac_alg': 'SHA256',
        'log_level': 'info',
        'listen': '0.0.0.0:8080',
    }


@pytest.fixture()
def config_path(tmp_path, valid_config_dict) -> str:
    """Фикстура, создающая файл с валидным конфигом и возвращающая путь."""
    cfg = dict(valid_config_dict)
    cfg['secret'] = base64.b64encode(b'x' * 32).decode('ascii')
    p = tmp_path / 'config.json'
    p.write_text(json.dumps(cfg), encoding='utf-8')
    return str(p)
