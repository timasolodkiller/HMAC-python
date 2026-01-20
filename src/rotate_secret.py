"""Утилита для ротации секрета."""

import base64
import json
import secrets

from src.utils import get_config_path
from src.log.logger import setup_logger
from src.constants import LOG_NEW_SECRET, LOG_ROTATE_SUCCESS

CONFIG_PATH = get_config_path(__file__)

logger = setup_logger(__name__)


def generate_secret(length: int = 32) -> str:
    """Генерирует случайный секрет в формате base64."""
    random_bytes = secrets.token_bytes(length)
    return base64.b64encode(random_bytes).decode('ascii')


def rotate_secret(config_path: str = CONFIG_PATH):
    """Обновляет секрет в конфигурационном файле."""
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    new_secret = generate_secret()
    config['secret'] = new_secret

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    logger.info(LOG_ROTATE_SUCCESS)
    logger.debug(LOG_NEW_SECRET.format(new_secret[:10]))


if __name__ == '__main__':
    rotate_secret()
