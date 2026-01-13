"""Модуль с сервисом для подписи и проверки сообщений."""

import base64
import hashlib
import hmac

from src.config import SETTINGS
from src.log.log_messages import (
    LOG_MSG_SIGNED,
    LOG_SECRET_DECODED,
    LOG_SIGN_COMPLETE,
    LOG_SIGN_START,
    LOG_SIGNATURE_INVALID,
    LOG_SIGNATURE_VALID,
    LOG_SIGNER_INIT,
)
from src.log.logger import setup_logger

logger = setup_logger(__name__)


class HMACSigner:
    """Класс для подписи и проверки сообщений."""

    def __init__(self, secret_key: str):
        """Инициализация с секретным ключом."""
        self.secret_key = base64.b64decode(secret_key)
        logger.debug(LOG_SECRET_DECODED)
        logger.info(LOG_SIGNER_INIT)

    def sign(self, msg: str) -> bytes:
        """Подписывает сообщение."""
        logger.debug(LOG_SIGN_START.format(len(msg)))

        result = hmac.new(
            self.secret_key, msg.encode('utf-8'), hashlib.sha256
        ).digest()

        logger.debug(LOG_SIGN_COMPLETE.format(len(result)))
        logger.info(LOG_MSG_SIGNED)
        return result

    def verify(self, msg: str, signature: bytes) -> bool:
        """Проверяет подпись сообщения."""
        computed_signature = self.sign(msg)
        result = hmac.compare_digest(computed_signature, signature)

        if result:
            logger.info(LOG_SIGNATURE_VALID)
        else:
            logger.warning(LOG_SIGNATURE_INVALID)

        return result


def hmac_service() -> HMACSigner:
    """Фабричная функция для создания HMACSigner."""
    return HMACSigner(SETTINGS.secret)