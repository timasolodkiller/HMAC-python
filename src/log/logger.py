"""Модуль для настройки логирования."""

import logging
import os
from logging.handlers import RotatingFileHandler

from src.config import SETTINGS

MAX_LOG_FILE_SIZE_MB = 5 * 1024 * 1024
BACKUP_COUNT = 5


def setup_logger(name: str, log_dir: str = 'logs') -> logging.Logger:
    """Создаёт и настраивает логгер."""
    root = logging.getLogger(name)
    level_name = SETTINGS.log_level.upper()
    root.setLevel(level_name)
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, 'app.log')
    if root.handlers:
        root.handlers.clear()

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=MAX_LOG_FILE_SIZE_MB,
        backupCount=BACKUP_COUNT,
        encoding='utf-8',
    )
    file_handler.setFormatter(formatter)

    root.addHandler(file_handler)

    return root
