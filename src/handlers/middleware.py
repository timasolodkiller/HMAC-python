"""Модуль с middleware для проверки запросов."""

from starlette.middleware.base import BaseHTTPMiddleware

from src.handlers.errors import BODY_TOO_LARGE, UNPROCESS_ENTITY
from src.handlers.json_response_builder import build_json_response
from src.log.log_messages import (
    LOG_BODY_TOO_LARGE,
    LOG_CONTENT_LENGTH_INVALID,
    LOG_INVALID_CONTENT_TYPE,
)
from src.log.logger import setup_logger

logger = setup_logger(__name__)

URLS_TO_CHECK = ('/sign', '/verify')


class EnforceJSONMiddleware(BaseHTTPMiddleware):
    """Middleware для проверки Content-Type: application/json."""

    async def dispatch(self, request, call_next):
        """Обрабатывает запрос и проверяет заголовок Content-Type."""
        if request.url.path in URLS_TO_CHECK:
            ct = request.headers.get('content-type', '')
            if not ct.lower().startswith('application/json'):
                logger.warning(LOG_INVALID_CONTENT_TYPE.format(ct))
                return build_json_response(UNPROCESS_ENTITY)
        return await call_next(request)


class BodySizeLimitMiddleware(BaseHTTPMiddleware):
    """Middleware для ограничения размера тела запроса."""

    def __init__(self, app, max_bytes_size_int: int):
        """Инициализация с максимальным размером в байтах."""
        super().__init__(app)
        self.max_bytes_size_int = max_bytes_size_int

    async def dispatch(self, request, call_next):
        """Обрабатывает запрос и проверяет размер тела."""
        if request.url.path in URLS_TO_CHECK:
            content_length = request.headers.get('content-length')
            if content_length is not None:
                try:
                    length = int(content_length)
                    if length > self.max_bytes_size_int:
                        logger.warning(
                            LOG_BODY_TOO_LARGE.format(length, self.max_bytes_size_int)
                        )
                        return build_json_response(BODY_TOO_LARGE)
                except ValueError:
                    logger.warning(LOG_CONTENT_LENGTH_INVALID.format(content_length))
        return await call_next(request)