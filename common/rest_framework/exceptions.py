from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler

from common.messages import INTERNAL_SERVER_ERROR_MESSAGE
from common.logging import LogInfo
from common.rest_framework.mixins import APIViewResponseMixin


class BaseCustomException(APIException):
    """
    Base custom exception class that inherits from APIException.
    Attributes:
        status_code (int): HTTP status code for the exception.
        detail (str): Details or message associated with the exception.
    """

    status_code = None
    detail = None

    def __init__(self, detail, status_code):
        """
        Initialize the custom exception.
        Args:
            detail (str): Details or message associated with the exception.
            status_code (int): HTTP status code for the exception.
        """
        super().__init__(detail, status_code)
        self.detail = detail
        self.status_code = status_code


def custom_exception_handler(exc, context):
    """
    Custom exception handler to handle and format exceptions globally.
    Args:
        exc (Exception): The exception raised.
        context (dict): Context information for the exception.
    Returns:
        Response: Customized response object.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now customize the response format.
    if response is not None:
        # Extract information from the original response
        status_code = response.status_code
        # Use gettext_lazy for localization and translation
        message = response.data.get('detail', INTERNAL_SERVER_ERROR_MESSAGE)
        if status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
            LogInfo.exception(exc)

        # Utilize gettext_lazy for localization and translation in the response
        return APIViewResponseMixin.failure_response(status_code=status_code, message=message, data=response.data)

    LogInfo.exception(exc)
    # Utilize gettext_lazy for localization and translation in the response
    return APIViewResponseMixin.failure_response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                                                 message=INTERNAL_SERVER_ERROR_MESSAGE, data=None)


class InvalidFilterValue(BaseCustomException):
    """Invalid Filter Value Error"""
    pass
