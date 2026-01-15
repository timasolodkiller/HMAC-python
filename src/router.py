"""Модуль с роутами API."""

from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.codec import decode_signature, encode_signature
from src.hmac_service import HMACSigner, hmac_service
from src.log.log_messages import (
    LOG_REQUEST_BODY,
    LOG_SIGN_REQUEST,
    LOG_SIGN_SUCCESS,
    LOG_VERIFY_BODY,
    LOG_VERIFY_REQUEST,
    LOG_VERIFY_RESULT,
)
from src.log.logger import setup_logger
from src.models import SignRequest, VerifyRequest
from src.validators.validators import check_msg, check_signature
from src.config import SETTINGS


logger = setup_logger(__name__)
router = APIRouter()


@router.post('/sign')
async def sign(
    request: SignRequest,
    hmac_service: Annotated[HMACSigner, Depends(hmac_service)],
):
    """Подписывает сообщение."""
    logger.debug(LOG_REQUEST_BODY.format(len(request.msg)))
    logger.info(LOG_SIGN_REQUEST)

    check_msg(request.msg, SETTINGS.max_msg_size_bytes)
    sig_bytes = hmac_service.sign(request.msg)
    sig_str = encode_signature(sig_bytes)

    logger.info(LOG_SIGN_SUCCESS)
    return JSONResponse({'signature': sig_str})


@router.post('/verify')
async def verify(
    request: VerifyRequest,
    hmac_service: Annotated[HMACSigner, Depends(hmac_service)],
):
    """Проверяет подпись сообщения."""
    logger.debug(LOG_VERIFY_BODY.format(len(request.msg),
                                        len(request.signature)))
    logger.info(LOG_VERIFY_REQUEST)

    check_msg(request.msg, SETTINGS.max_msg_size_bytes)
    check_signature(request.signature)

    sig_bytes = decode_signature(request.signature)
    result = hmac_service.verify(request.msg, sig_bytes)

    logger.info(LOG_VERIFY_RESULT.format(result))
    return JSONResponse({'ok': result})
