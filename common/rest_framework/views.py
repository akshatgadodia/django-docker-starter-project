from io import TextIOWrapper
from rest_framework.mixins import ListModelMixin
from rest_framework import status, filters

from common.rest_framework import generics
from common.rest_framework import mixins
from common.rest_framework.filters import QueryFilterBackend
from common.rest_framework.serializers import DropdownItemSerializer


class DropdownListAPIView(generics.BaseAPIView, mixins.APIViewResponseMixin):
    serializer_class = DropdownItemSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        return self.success_response(data=data)
