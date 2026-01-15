"""Константы кодов ошибок."""

from fastapi import status

INVALID_MSG = 'invalid_msg'
INVALID_SIGNATURE = 'invalid_signature_format'
BODY_TOO_LARGE = 'payload_too_large'
UNPROCESS_ENTITY = 'invalid_content_type'
INVALID_JSON = 'invalid_json'
INTERNAL_ERROR = 'internal_error'

STATUS_BY_CODE = {
    UNPROCESS_ENTITY: status.HTTP_422_UNPROCESSABLE_CONTENT,
    INVALID_JSON: status.HTTP_400_BAD_REQUEST,
    INVALID_MSG: status.HTTP_400_BAD_REQUEST,
    INVALID_SIGNATURE: status.HTTP_400_BAD_REQUEST,
    BODY_TOO_LARGE: status.HTTP_413_CONTENT_TOO_LARGE,
    INTERNAL_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
}
