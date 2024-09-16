from typing import Optional, Any

from rest_framework import status
from rest_framework.exceptions import (
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
    NotFound,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler

from core.utils.error_messages import (
    VALIDATION_ERROR_MSG,
    PERMISSION_DENIED_ERROR_MSG,
    NOT_AUTHENTICATED_ERROR_MSG,
    AUTHENTICATION_FAILED_ERROR_MSG,
    NOT_FOUND_ERROR_MSG,
)


def custom_exception_handler(exc: Exception, context: dict[str, Any]) -> Optional[Response]:
    # 기본 예외처리 호출
    response = exception_handler(exc, context)

    # ValidationError 처리: 입력 데이터에 대한 처리
    if isinstance(exc, ValidationError):
        return Response(
            VALIDATION_ERROR_MSG,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # PermissionDenied 처리
    if isinstance(exc, PermissionDenied):
        return Response(
            PERMISSION_DENIED_ERROR_MSG,
            status=status.HTTP_403_FORBIDDEN,
        )

    # NotAuthenticated 처리:
    if isinstance(exc, NotAuthenticated):
        return Response(
            NOT_AUTHENTICATED_ERROR_MSG,
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # AuthenticationFailed 처리
    if isinstance(exc, AuthenticationFailed):
        return Response(
            AUTHENTICATION_FAILED_ERROR_MSG,
            status=status.HTTP_401_UNAUTHORIZED,
        )

    # NotFound 처리: DB에 데이터가 존재하지 않는 경우
    if isinstance(exc, NotFound):
        return Response(
            NOT_FOUND_ERROR_MSG,
            status=status.HTTP_404_NOT_FOUND,
        )

    return response
