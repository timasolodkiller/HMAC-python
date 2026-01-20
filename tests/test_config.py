"""Тестирование конфига."""
import json

import pytest

from .messages import SETTINGS_ATTRS_ERROR, SETTINGS_HAVING_ERROR
from src.config import load_settings
from src.models import Settings
from src.exceptions.exceptions import ConfigError

NOT_BASE_64_SECRET = 'NOT_BASE64!!!'


def test_load_settings_ok(config_path):
    """Проверка, что конфиг корректно загружается."""
    settings = load_settings(config_path)
    assert isinstance(settings, Settings), SETTINGS_HAVING_ERROR

    cfg = json.loads(open(config_path, encoding="utf-8").read())
    for key, expected in cfg.items():
        assert getattr(settings, key) == expected, SETTINGS_ATTRS_ERROR


def test_load_settings_file_not_found(tmp_path):
    """Проверка, что если конфига нет, что программа выбрасывает исключение."""
    with pytest.raises(ConfigError):
        load_settings(str(tmp_path / 'missing.json'))


def test_load_settings_invalid_json(tmp_path, valid_config_dict):
    """Проверка, что если JSON не валидного формата.

    Программа должна остановиться.
    """
    config_path = tmp_path / 'config.json'
    config_path.write_text('{not json', encoding='utf-8')

    with pytest.raises(ConfigError):
        load_settings(str(config_path))


def test_load_settings_missing_field(config_path):
    """Проверка, что если нет какого-либо атрибута то программа остановится."""
    cfg = json.loads(open(config_path, encoding="utf-8").read())
    cfg.pop('port', None)
    open(config_path, "w", encoding="utf-8").write(json.dumps(cfg))

    with pytest.raises(ConfigError):
        load_settings(config_path)


def test_load_settings_invalid_secret(config_path):
    """Проверка, что если секрет не валидный то программа остановится."""
    cfg = json.loads(open(config_path, encoding="utf-8").read())
    cfg['secret'] = NOT_BASE_64_SECRET
    open(config_path, "w", encoding="utf-8").write(json.dumps(cfg))

    with pytest.raises(ConfigError):
        load_settings(config_path)
