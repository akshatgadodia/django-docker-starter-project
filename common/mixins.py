from rest_framework import status
from rest_framework.response import Response


class APIViewResponseMixin:
    @classmethod
    def success_response(cls, message=None, data=None, status_code=status.HTTP_200_OK):
        response_data = {
            "status_code": status_code,
            "message": message,
            "data": data
        }
        return Response(response_data, status=status_code)

    @classmethod
    def failure_response(cls, message=None, data=None, status_code=status.HTTP_200_OK):
        response_data = {
            "status_code": status_code,
            "message": message,
            "data": data
        }
        return Response(response_data, status=status_code)
