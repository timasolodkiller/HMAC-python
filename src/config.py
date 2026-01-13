"""Загрузка переменных из config."""

import json
import logging
import sys

from src.log.log_messages import (
    LOG_CONFIG_LOADED,
    LOG_CONFIG_LOAD_ERROR,
    LOG_CONFIG_NOT_FOUND,
    LOG_CONFIG_PARSE_ERROR,
)
from src.log.logger import setup_logger
from .models import Settings


logger = setup_logger(__name__)

try:
    with open('config.json', 'r', encoding='utf-8') as f:
        cfg = json.load(f)
    SETTINGS = Settings(**cfg)
    logger.info(LOG_CONFIG_LOADED)
except FileNotFoundError:
    logger.critical(LOG_CONFIG_NOT_FOUND)
    sys.exit(1)
except json.JSONDecodeError as e:
    logger.critical(LOG_CONFIG_PARSE_ERROR.format(e))
    sys.exit(1)
except Exception as e:
    logger.critical(LOG_CONFIG_LOAD_ERROR.format(e))
    sys.exit(1)