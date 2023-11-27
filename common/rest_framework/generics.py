from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import status
from base.mixins import APIViewResponseMixin
from base.pagination import StandardResultsSetPagination


class BaseAPIView(GenericAPIView, APIViewResponseMixin):
    pagination_class = StandardResultsSetPagination


class BaseListAPIView(BaseAPIView, ListAPIView):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        data = self.get_paginated_response(serializer.data)
        return self.success_response(data=data, message=None, status_code=status.HTTP_200_OK)