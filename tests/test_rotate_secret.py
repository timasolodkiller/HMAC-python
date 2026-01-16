"""Тесты rotate_secret."""
import base64
import json

from src.rotate_secret import rotate_secret
from .messages import VALID_SECRET, NOT_CHANGED_SECRET


def test_rotate_secret_updates_secret_and_keeps_other_fields(config_path):
    """Тест, что новый секрет подставляется в конфиг."""
    before = json.loads(open(config_path, 'r', encoding='utf-8').read())
    old_secret = before['secret']

    rotate_secret(config_path)

    after = json.loads(open(config_path, 'r', encoding='utf-8').read())
    new_secret = after['secret']
    assert after['secret'] != old_secret and after['secret'] == new_secret, (
        NOT_CHANGED_SECRET
    )
    before.pop('secret')
    after.pop('secret')
    assert after == before, NOT_CHANGED_SECRET


def test_rotate_secret_generates_valid_base64(config_path):
    """Тест, что подставляется только валидный секрет в конфиг."""
    rotate_secret(config_path)
    new_secret = json.loads(
        open(config_path, 'r', encoding='utf-8').read()
    )['secret']
    raw = base64.b64decode(new_secret, validate=True)
    assert len(raw) == 32, VALID_SECRET
