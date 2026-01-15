"""Тестирование конфига."""
import json

import pytest

from .messages import SETTINGS_ATTRS_ERROR, SETTINGS_HAVING_ERROR
from src.config import load_settings
from src.models import Settings
from src.exceptions.exceptions import ConfigError


def test_load_settings_ok(tmp_path, valid_config_dict):
    """Проверка, что конфиг корректно загружается."""
    p = tmp_path / 'config.json'
    p.write_text(json.dumps(valid_config_dict), encoding='utf-8')

    s = load_settings(str(p))
    assert isinstance(s, Settings), SETTINGS_HAVING_ERROR
    assert s.port == 8080, SETTINGS_ATTRS_ERROR
    assert s.max_msg_size_bytes == 1048576, SETTINGS_ATTRS_ERROR


def test_load_settings_file_not_found(tmp_path):
    """Проверка, что если конфига нет, что программа выбрасывает исключение."""
    with pytest.raises(ConfigError):
        load_settings(str(tmp_path / 'missing.json'))


def test_load_settings_invalid_json(tmp_path):
    """Проверка, что если JSON не валидного формата."""
    """Программа должна остановиться."""
    p = tmp_path / 'config.json'
    p.write_text('{not json', encoding='utf-8')

    with pytest.raises(ConfigError):
        load_settings(str(p))


def test_load_settings_missing_field(tmp_path, valid_config_dict):
    """Проверка. что если нет какого-либо атрибута то программа остановится."""
    cfg = dict(valid_config_dict)
    cfg.pop('port')

    p = tmp_path / 'config.json'
    p.write_text(json.dumps(cfg), encoding='utf-8')

    with pytest.raises(ConfigError):
        load_settings(str(p))


def test_load_settings_invalid_secret(tmp_path, valid_config_dict):
    """Проверка. что если секрет не валидный то программа остановится."""
    cfg = dict(valid_config_dict)
    cfg['secret'] = 'NOT_BASE64!!!'

    p = tmp_path / 'config.json'
    p.write_text(json.dumps(cfg), encoding='utf-8')

    with pytest.raises(ConfigError):
        load_settings(str(p))
