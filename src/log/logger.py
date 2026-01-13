"""Модуль для настройки логирования."""

import json
import logging
import sys


def _get_log_level() -> int:
    """Получает уровень логирования из конфига."""
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        level_name = cfg.get('log_level', 'info').upper()
        return getattr(logging, level_name, logging.INFO)
    except Exception:
        return logging.INFO


def setup_logger(name: str) -> logging.Logger:
    """Создаёт и настраивает логгер."""
    logger = logging.getLogger(name)
    logger.setLevel(_get_log_level())

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger