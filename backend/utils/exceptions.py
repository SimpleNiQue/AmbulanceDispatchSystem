import enum
import logging
from typing import Dict, Optional, Union

from rest_framework import status
from rest_framework.exceptions import (
    APIException,
    AuthenticationFailed,
    NotAuthenticated,
    PermissionDenied,
    ValidationError,
)
from rest_framework.response import Response
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is None:
        return Response({"error": "url not found"}, status=status.HTTP_404_NOT_FOUND)

    return response


class BaseAPIException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "An error occurred."
    default_code = "error"

    def __init__(
        self, message=None, status_code=status.HTTP_400_BAD_REQUEST, data=None
    ):
        self.status_code = status_code
        self.detail = {
            "status": self.status_code,
            "message": message or self.default_detail,
            "data": data or None,
        }

    def get_response(self):
        return Response(self.detail, status=self.status_code)


class BadRequestError(BaseAPIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "An error occurred, please check your data and try again"


class NotFoundError(BaseAPIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Resource not found."


class SendEmailError(BaseAPIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "Failed to send email, please try again."


class CustomExceptions(enum.Enum):
    BAD_REQUEST = (
        BadRequestError,
        "Invalid request data.",
        status.HTTP_400_BAD_REQUEST,
    )
    UNAUTHORIZED = (
        NotAuthenticated,
        "Not authorized",
        status.HTTP_401_UNAUTHORIZED,
    )
    NOT_FOUND = (
        NotFoundError,
        "Resource not found",
        status.HTTP_404_NOT_FOUND,
    )
    VALIDATION_ERROR = (
        ValidationError,
        "Invalid data.",
        status.HTTP_400_BAD_REQUEST,
    )
    AUTHENTICATION_ERROR = (
        AuthenticationFailed,
        "Authentication failed",
        status.HTTP_401_UNAUTHORIZED,
    )
    EMAIL_ERROR = (
        SendEmailError,
        "Failed to send email",
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
    PERMISSION_DENIED = (
        PermissionDenied,
        "Youre not authenticated for this",
        status.HTTP_403_FORBIDDEN,
    )

    def __init__(self, exception_class, message, status_code):
        self.exception_class = exception_class
        self.message = message
        self.status_code = status_code


def handle_exception(
    message: Optional[str] = None,
    exception_enum: Optional[CustomExceptions] = CustomExceptions.BAD_REQUEST,
    logger_name: str = __name__,
    *,
    exception: Optional[Exception] = None,
    data: Optional[Dict[str, Union[str, int, float, dict, list]]] = None,
) -> None:
    """
    Handles exceptions by logging and raising the appropriate custom exception.

    :param exception: The actual exception instance.
    :param exception_enum: The predefined CustomExceptions enum (optional).
    :param logger_name: Name of the logger to use.
    :param message: Custom error message (overrides default if provided).
    :param data: Additional data to attach to the exception.
    """

    # Determine the exception details
    if exception_enum:
        exception_class = exception_enum.exception_class
        message = message or exception_enum.message  # Use custom message if provided
        status_code = exception_enum.status_code
    elif isinstance(exception, BaseAPIException):
        # If it's already a known custom exception, use its properties
        exception_class = type(exception)
        message = message or exception.message
        status_code = exception.status_code
    else:
        # Default fallback (if no enum provided)
        exception_class = BaseAPIException
        message = message or "An unexpected error occurred."
        status_code = 400

    # Log the error
    if exception:
        logger = logging.getLogger(logger_name)
        log_message = f"{message}: {exception}"

        if data:
            log_message += f" | Extra Data: {data}"
        logger.error(log_message)

    # Raise the exception with optional extra data
    raise exception_class(message=message, status_code=status_code, data=data)
