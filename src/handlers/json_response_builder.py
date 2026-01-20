"""Модуль для шортката построения ответа сервиса."""

from fastapi.responses import JSONResponse

from src.constants import STATUS_BY_CODE


def build_json_response(code: str):
    """Функция построения ответа сервиса."""
    return JSONResponse(status_code=STATUS_BY_CODE[code],
                        content={'error': code})
