# HMAC: подпись и проверка сообщений (HMAC-SHA256)

Минимальный REST-сервис на FastAPI для подписи и проверки целостности сообщений с помощью **HMAC-SHA256**.  
Секрет хранится в локальном файле `config.json`. Подпись возвращается в формате **base64url без паддинга**.

## Что умеет сервис

- `POST /sign` — подписывает сообщение и возвращает подпись.
- `POST /verify` — проверяет подпись сообщения и возвращает `ok: true|false`.
- Ограничение размера входных данных (`max_msg_size_bytes`) для защиты от DoS.
- Тайминг-стойкое сравнение подписи (`hmac.compare_digest`).
- Логи валидных операций и ошибок (без утечки секрета).
- Утилита для ротации секрета `rotate_secret.py`.

---

## Требования к окружению

- Python 3.11+ (рекомендуется)
- Менеджер зависимостей: **uv**
- `make`

### Установка uv

Установите `uv` по инструкции из репозитория Astral:  
https://github.com/astral-sh/uv?tab=readme-ov-file#installation

---

## Установка зависимостей

Установка зависимостей через Make:

```bash
make sync
```

---

## Конфигурация `config.json`

Файл конфигурации должен лежать в корне проекта: `./config.json`.

Пример:

```json
{
  "host": "0.0.0.0",
  "port": 8080,
  "max_msg_size_bytes": 1048576,
  "secret": "c2VjcmV0",
  "hmac_alg": "SHA256",
  "log_level": "info",
  "listen": "0.0.0.0:8080"
}
```

### Поля

- `secret` — секрет в формате **base64** (строго валидный base64).
- `max_msg_size_bytes` — максимальный допустимый размер сообщения (защита от DoS).
- `log_level` — уровень логирования (`debug`, `info`, `warning`, `error`, `critical`).
- `hmac_alg` — алгоритм HMAC (фиксирован `SHA256` в рамках задания).
- `host`, `port`, `listen` — параметры для запуска (используются в команде запуска).

### Рекомендация по правам на файл

Для Unix-систем:

```bash
chmod 600 config.json
```

---

## Запуск сервера

Поднять сервер с API:

```bash
make run/api
```

После старта сервис будет доступен (по умолчанию) на `http://localhost:8080`.

---

## Примеры запросов (curl)

### Подписать сообщение

```bash
curl -sS -X POST http://localhost:8080/sign   -H 'Content-Type: application/json'   -d '{"msg":"hello"}'
```

Пример ответа:

```json
{
  "signature": "AAECAwQFBgcICQoLDA0ODxAREhMUFRYXGBkaGxwdHh8"
}
```

> `signature` — base64url без `=` (без паддинга).

### Проверить подпись

```bash
curl -sS -X POST http://localhost:8080/verify   -H 'Content-Type: application/json'   -d '{"msg":"hello","signature":"<signature_from_sign>"}'
```

Ответ при совпадении:

```json
{ "ok": true }
```

Ответ при несовпадении:

```json
{ "ok": false }
```

---

## Ошибки и коды ответов

Сервис возвращает ошибки в формате:

```json
{ "detail": "<error_code>" }
```

Типовые коды HTTP:

- `400 Bad Request` — невалидный `msg` или `signature`.
- `413 Payload Too Large` — превышен лимит размера входных данных.
- `422 Unprocessable Entity` — неверный `Content-Type` (не `application/json`).
- `500 Internal Server Error` — непредвиденная ошибка.

Типовые `detail`-коды (смысловые):

- `invalid_json` — тело запроса не является корректным JSON.
- `invalid_msg` — `msg` пустой/не строка/некорректен.
- `invalid_signature_format` — подпись не base64url или декодируется не в 32 байта.
- `payload_too_large` — сообщение превышает `max_msg_size_bytes`.
- `invalid_content_type` — неверный `Content-Type` для `/sign` и `/verify`.
- `internal` — внутренняя ошибка сервиса.

---

## Как работает подпись (кратко)

1. Сообщение `msg` преобразуется в `UTF-8` байты.
2. Вычисляется `HMAC-SHA256`:
   - `sig = hmac.new(key, msg, hashlib.sha256).digest()`
3. Подпись кодируется в base64url без паддинга:
   - `base64.urlsafe_b64encode(sig).rstrip(b"=").decode("ascii")`

---

## Ротация секрета

В проекте есть утилита ротации секрета, которая:
- генерирует новый секрет
- записывает его в `config.json`

Запуск:

```bash
python src/rotate_secret.py
```

Скрипт выведет сообщение об успешной замене и покажет начало нового секрета.

---

## Запуск тестов

Тесты запускаются через Make:

```bash
make test
```

В набор входят:
- HTTP-тесты роутера (`/sign`, `/verify`)
- юнит-тесты `hmac_service`
- юнит-тесты `codec`
- тесты загрузки `config`

---

## Логи

Логирование выводится в stdout и содержит:
- валидные операции (`/sign`, `/verify`)
- ошибки валидации и неожиданные исключения

Секрет и полные входные данные не логируются (в логах используется длина).

---

## Структура проекта (упрощённо)

- `src/app.py` — создание FastAPI приложения, middleware, handlers
- `src/router.py` — эндпоинты `/sign` и `/verify`
- `src/hmac_service.py` — HMACSigner: подпись/проверка
- `src/codec.py` — base64url encode/decode + валидация подписи
- `src/config.py` — загрузка настроек и `get_settings()`
- `src/models.py` — модели запросов/ответов и Settings
- `src/handlers/*` — обработчики ошибок, middleware
- `src/rotate_secret.py` — утилита ротации секрета
- `tests/*` — тесты

---

## Ограничения учебной реализации

- Это **не шифрование**: сообщение передаётся открытым текстом.
- Это **не асимметричная** электронная подпись (нет сертификатов, цепочек доверия, неотказуемости).
- Без БД: используется только локальный файл конфигурации.
- Без многоключевой валидации: один общий секрет.

---

## Автор
timasolodkiller - github
