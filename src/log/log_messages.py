"""Константы сообщений для логирования."""

# INFO сообщения
LOG_SIGNER_INIT = 'HMACSigner инициализирован'
LOG_SIGN_REQUEST = 'POST /sign'
LOG_SIGN_SUCCESS = 'POST /sign — успех'
LOG_VERIFY_REQUEST = 'POST /verify'
LOG_VERIFY_RESULT = 'POST /verify — ok={}'
LOG_CONFIG_LOADED = 'Конфигурация загружена успешно'
LOG_MSG_SIGNED = 'Сообщение успешно подписано'
LOG_SIGNATURE_VALID = 'Подпись валидна'

# DEBUG сообщения
LOG_REQUEST_BODY = 'Тело запроса получено, msg длина: {}'
LOG_VERIFY_BODY = 'Тело запроса: msg={}, sig={}'
LOG_MSG_VALID = 'Сообщение валидно, размер: {} байт'
LOG_SIGNATURE_FORMAT_VALID = 'Формат подписи валиден'
LOG_SIGN_START = 'Начало подписи, длина msg: {} байт'
LOG_SIGN_COMPLETE = 'Подпись создана, длина: {} байт'
LOG_SECRET_DECODED = 'Секрет успешно декодирован из base64'

# WARNING сообщения
LOG_EMPTY_MSG = 'Получено пустое или невалидное сообщение'
LOG_MSG_TOO_LARGE = 'Сообщение слишком большое: {} > {}'
LOG_INVALID_SIGNATURE_FORMAT = 'Невалидный формат подписи, длина: {}'
LOG_SIGNATURE_INVALID = 'Подпись НЕ валидна!'
LOG_APP_ERROR = 'Ошибка приложения: {}'
LOG_INVALID_CONTENT_TYPE = 'Неверный Content-Type: {}'
LOG_BODY_TOO_LARGE = 'Тело запроса слишком большое: {} > {}'
LOG_CONTENT_LENGTH_INVALID = 'Невалидный Content-Length: {}'

# ERROR сообщения
LOG_VALIDATION_ERROR = 'Ошибка валидации запроса: {}'

# CRITICAL сообщения
LOG_CONFIG_NOT_FOUND = 'Файл config.json не найден!'
LOG_CONFIG_PARSE_ERROR = 'Ошибка парсинга config.json: {}'
LOG_CONFIG_LOAD_ERROR = 'Ошибка загрузки конфига: {}'
LOG_UNEXPECTED_ERROR = 'Непредвиденная ошибка: {}: {}'
LOG_CONFIG_NOT_FOUND = 'Файл config.json не найден!'
LOG_CONFIG_PARSE_ERROR = 'Ошибка парсинга config.json: {}'
LOG_CONFIG_LOAD_ERROR = 'Ошибка загрузки конфига: {}'
LOG_CONFIG_LOADED = 'Конфигурация загружена успешно'
LOG_CONFIG_MISSING_FIELD = 'Отсутствует обязательное поле в config.json: {}'