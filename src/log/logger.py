"""Модуль для настройки логирования."""

import logging
import sys

from src.config import SETTINGS


def setup_logger(name: str) -> logging.Logger:
    """Создаёт и настраивает логгер."""
    logger = logging.getLogger(name)
    level_name = SETTINGS.log_level.upper()
    logger.setLevel(level_name)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
