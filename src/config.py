"""Загрузка переменных из config."""

import json
from typing import Optional

from src.utils import get_config_path
from src.models import Settings
from src.exceptions.exceptions import ConfigError


CONFIG_PATH = get_config_path(__file__)


def load_settings(config_path: Optional[str] = None) -> Settings:
    """Загрузка настроек из config."""
    path = config_path or get_config_path(__file__)

    try:
        with open(path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
    except FileNotFoundError as e:
        raise ConfigError('config_not_found') from e
    except json.JSONDecodeError as e:
        raise ConfigError('invalid_json') from e
    except Exception as e:
        raise ConfigError('config_load_error') from e
    try:
        settings = Settings(**cfg)
    except Exception as e:
        raise ConfigError('invalid_config_fields') from e
    return settings


SETTINGS = load_settings()
