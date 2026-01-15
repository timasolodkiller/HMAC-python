"""Модуль с обработчиками исключений для FastAPI."""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from src.exceptions.exceptions import AppError
from src.log.log_messages import (
    LOG_APP_ERROR,
    LOG_UNEXPECTED_ERROR,
    LOG_VALIDATION_ERROR,
)
from src.log.logger import setup_logger

from .errors import INVALID_JSON, INVALID_MSG, INVALID_SIGNATURE
from .json_response_builder import build_json_response

logger = setup_logger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    """Регистрирует обработчики исключений."""

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ):
        """Обрабатывает ошибки валидации запроса."""
        logger.error(LOG_VALIDATION_ERROR.format(exc.errors()))

        errors = exc.errors()
        if any(
            e.get('type') in {'json_invalid', 'value_error.jsondecode'}
            for e in errors
        ):
            return build_json_response(INVALID_JSON)
        if any('msg' in e.get('loc', ()) for e in errors):
            return build_json_response(INVALID_MSG)
        if any('signature' in e.get('loc', ()) for e in errors):
            return build_json_response(INVALID_SIGNATURE)
        return build_json_response(INVALID_JSON)

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        """Обрабатывает ошибки приложения."""
        logger.warning(LOG_APP_ERROR.format(exc.code))
        return build_json_response(exc.code)

    @app.exception_handler(Exception)
    async def general_error_handler(request: Request, exc: Exception):
        """Обрабатывает непредвиденные ошибки."""
        logger.critical(LOG_UNEXPECTED_ERROR.format(type(exc).__name__, exc))
        return build_json_response('internal')
