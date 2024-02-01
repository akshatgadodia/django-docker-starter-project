from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import status

from common.rest_framework.mixins import APIViewResponseMixin
from common.rest_framework.pagination import StandardResultsSetPagination


class BaseAPIView(GenericAPIView, APIViewResponseMixin):
    """
    Base API view that inherits from GenericAPIView and includes custom response mixins.
    """

    def get_serializer_context(self):
        """
        Override this method to pass the request object as context to the serializer.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class BaseListAPIView(BaseAPIView, ListAPIView):
    """
    Base List API view that inherits from BaseAPIView and ListAPIView.
    Includes standard pagination using StandardResultsSetPagination.
    """
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        """
        Custom list view method to handle list requests.
        Args:
            request (Request): The incoming request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        Returns:
            Response: Customized response object.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        data = self.get_paginated_response(serializer.data)
        return self.success_response(data=data, status_code=status.HTTP_200_OK)
