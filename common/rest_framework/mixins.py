from rest_framework import status
from rest_framework.response import Response

from common.constants import SUCCESS, FAILED


class APIViewResponseMixin:
    """
    Mixin class for generating consistent API responses.
    """

    @classmethod
    def success_response(cls, message=None, data=None, status_code=status.HTTP_200_OK):
        """
        Generates a successful API response.
        Args:
            message (str): A message providing additional information about the success.
            data (dict): Additional data to include in the response.
            status_code (int): HTTP status code for the response.
        Returns:
            Response: A Response object representing a successful API response.
        """
        response_data = {
            "status": SUCCESS,
            "status_code": status_code,
            "data": {
                **({"message": message} if message is not None else {}),
                **({"data": data} if not isinstance(data, dict) else data)
            }
        }
        return Response(response_data, status=status_code)

    @classmethod
    def failure_response(cls, message=None, data=None, status_code=status.HTTP_200_OK):
        """
        Generates a failure API response.
        Args:
            message (str): A message providing additional information about the failure.
            data (dict): Additional data to include in the response.
            status_code (int): HTTP status code for the response.
        Returns:
            Response: A Response object representing a failure API response.
        """
        response_data = {
            "status": FAILED,
            "status_code": status_code,
            "data": {
                **({"message": message} if message is not None else {}),
                **({"data": data} if not isinstance(data, dict) else data)
            }
        }
        return Response(response_data, status=status_code)
