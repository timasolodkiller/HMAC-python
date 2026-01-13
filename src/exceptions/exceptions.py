"""Модуль с пользовательскими исключениями приложения."""


class AppError(Exception):
    """Исключение приложения с кодом ошибки."""

    def __init__(self, code: str):
        """Инициализация с кодом ошибки."""
        self.code = code
        super().__init__(code)
