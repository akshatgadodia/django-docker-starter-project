from rest_framework.exceptions import APIException
from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.response import Response
from base.messages import INTERNAL_SERVER_ERROR_MESSAGE


# Custom base exception class that inherits from APIException
class BaseCustomException(APIException):
    status_code = None
    detail = None

    def __init__(self, detail, status_code):
        super().__init__(detail, status_code)
        self.detail = detail
        self.status_code = status_code


# Custom exception handler to handle and format exceptions globally
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now customize the response format.
    if response is not None:
        # Extract information from the original response
        status_code = response.status_code
        message = response.data.get('detail', INTERNAL_SERVER_ERROR_MESSAGE)

        # Create a custom response in a standardized format
        custom_response = {
            'status_code': status_code,
            'message': message,
            'data': response.data,
        }

        return Response(custom_response, status=status_code)

    # Create a custom response for the unhandled exception
    custom_response = {
        'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR,
        'message': INTERNAL_SERVER_ERROR_MESSAGE,
        'data': None,
    }

    return Response(custom_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
