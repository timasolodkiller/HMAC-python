"""Модуль работы приложения FastAPI."""

from fastapi import FastAPI

from src.handlers.middleware import (
    EnforceJSONMiddleware, BodySizeLimitMiddleware
)
from src.handlers.handlers import register_exception_handlers
from src.router import router
from src.config import SETTINGS

app = FastAPI()
app.include_router(router)
register_exception_handlers(app)
app.add_middleware(
    BodySizeLimitMiddleware, max_bytes_size_int=SETTINGS.max_msg_size_bytes
)
app.add_middleware(EnforceJSONMiddleware)
