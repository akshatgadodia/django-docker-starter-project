from rest_framework import serializers

from brands.messages import INVALID_ACTION
from common.logging import LogInfo
from common.messages import INTERNAL_SERVER_ERROR_MESSAGE
from common.rest_framework.messages import (FILE_NOT_PROVIDED, PROCESS_FILE_NOT_IMPLEMENTED, INVALID_OPERATION,
                                            INVALID_EXTENSION, FILE_EMAIL_SENT, EMAIL_NOT_FOUND, PERMISSION_DENIED)
from common.utils.file import generate_excel_from_html, generate_pdf_from_html
from common.tasks import send_report_email


class BaseSerializer(serializers.Serializer):

    def get_first_error(self):
        errors = self.errors
        if errors:
            for field, error_list in errors.items():
                if error_list:
                    return str(error_list[0])
        return INTERNAL_SERVER_ERROR_MESSAGE


class BaseModelSerializer(serializers.ModelSerializer):
    def set_user_field(self, field_name, instance, user, override=False):
        if override or not hasattr(instance, field_name):
            instance[field_name] = user

    def create(self, validated_data, set_user=True):
        if set_user:
            user = self.context['request'].user
            self.set_user_field('created_by', validated_data, user)
        return super().create(validated_data)

    def update(self, instance, validated_data, set_user=True):
        if set_user:
            user = self.context['request'].user
            self.set_user_field('updated_by', instance, user, True)
        return super().update(instance, validated_data)

    def get_first_error(self):
        errors = self.errors
        if errors:
            for field, error_list in errors.items():
                if error_list:
                    return str(error_list[0])
        return INTERNAL_SERVER_ERROR_MESSAGE


class DropdownItemSerializer(BaseSerializer):
    label = serializers.CharField(source="name")
    value = serializers.IntegerField(source="id")

    class Meta:
        fields = ('label', 'value')