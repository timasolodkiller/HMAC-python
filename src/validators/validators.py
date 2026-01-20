"""Модуль с функциями валидации входных данных."""

from src.codec import is_valid_base64url
from src.exceptions.exceptions import AppError
from src.constants import (
    LOG_EMPTY_MSG,
    LOG_INVALID_SIGNATURE_FORMAT,
    LOG_MSG_TOO_LARGE,
    LOG_MSG_VALID,
    LOG_SIGNATURE_FORMAT_VALID,
    INVALID_MSG, INVALID_SIGNATURE
)
from src.log.logger import setup_logger

logger = setup_logger(__name__)


def check_msg(msg: str, max_bytes_size_int: int):
    """Проверяет корректность сообщения."""
    if not isinstance(msg, str) or msg.strip() == '':
        logger.warning(LOG_EMPTY_MSG)
        raise AppError(INVALID_MSG)

    msg_size = len(msg.encode('utf-8'))
    if msg_size > max_bytes_size_int:
        logger.warning(LOG_MSG_TOO_LARGE.format(msg_size, max_bytes_size_int))
        raise AppError(INVALID_MSG)

    logger.debug(LOG_MSG_VALID.format(msg_size))


def check_signature(signature: str):
    """Проверяет корректность формата подписи."""
    if not is_valid_base64url(signature):
        logger.warning(LOG_INVALID_SIGNATURE_FORMAT.format(len(signature)))
        raise AppError(INVALID_SIGNATURE)

    logger.debug(LOG_SIGNATURE_FORMAT_VALID)
