import datetime
from rest_framework import filters
from rest_framework.compat import coreapi
from rest_framework import status
from django.core.exceptions import FieldError, ValidationError
from common.rest_framework.exceptions import InvalidFilterValue
from common.utils.conversions import string_to_bool, int_or_zero


class QueryFilterBackend(filters.BaseFilterBackend):
    """Custom Backend for Query Filters"""
    def get_filtering(self,query_params, query_filters):
        """Validate and create filterset from the query params"""
        all_filters = {}
        for filter in query_filters:
            if filter.name in query_params:
                filter.value = query_params.get(filter.name)
                all_filters[filter.lookup] = filter.value
        return all_filters

    def filter_queryset(self, request, queryset, view):
        """Returns filtered queryset"""
        query_params = request.query_params.dict()
        query_filter_fields = getattr(view, 'query_filters', None)
        try:
            filters_dict = self.get_filtering(query_params, query_filter_fields)
            if filters_dict:
                return queryset.filter(**filters_dict)
        except FieldError as e:
            raise InvalidFilterValue(detail=str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except ValidationError as e:
            raise InvalidFilterValue(detail=e, status_code=status.HTTP_400_BAD_REQUEST)
        return queryset

    def get_schema_fields(self, view):
        return [
            coreapi.Field(
                name=filter.name,
                required=False,
                location='query',
            )
            for filter in view.query_filters
        ]
    def get_schema_operation_parameters(self, view):
        return [
            ({
                'name': filter.name,
                'required': False,
                'description': getattr(filter, 'description', ''),
                'in': 'query',
                'schema': {
                    'type': getattr(filter, 'schema_type', 'string'),
                },
            })
            for filter in view.query_filters
        ]


class BaseFilter:
    """Base Filter class for  validations"""
    def __init__(self, description='', *, name, lookup, cast=str):
        self.name = name
        self.lookup = lookup
        self.description = description
        self.cast = cast

    def clean(self, value):
        """ Validation logic goes here"""
        raise NotImplementedError("Clean Method should be Implemented")

    @property
    def value(self):
        clean_value = self.clean(self._value)

        # assert clean_value, "Clean Method Should return a Value"
        return clean_value

    @value.setter
    def value(self, value):
        self._value = value


class IntegerFilter(BaseFilter):
    def __init__(self, **kwargs):
        self.schema_type = 'integer'
        super().__init__(**kwargs)

    def clean(self, value):
        try:
            return int(value)
        except ValueError:
            raise ValidationError(f"{self.name} should be a Integer")


class CharFilter(BaseFilter):
    def __init__(self, **kwargs):
        self.filter_required = kwargs.pop('required')
        super().__init__(**kwargs)

    def clean(self, value):
        if not value.strip() and self.filter_required:
            raise ValidationError(f"{self.name} cannot be empty")
        return value.strip()


class ChoiceFilter(BaseFilter):
    def __init__(self, *, choices, **kwargs):
        self.choices = choices
        super().__init__(**kwargs)

    def clean(self, value):
        if value not in self.choices:
            raise ValidationError(f"{self.name} should be in {self.choices}")
        return value


class DateTimeFilter(BaseFilter):
    def __init__(self, **kwargs):
        self.schema_type = 'date'
        super().__init__(**kwargs)

    def clean(self, value):
        try:
            value = value.strip()
            datetime_object = datetime.datetime.fromisoformat(value)
            return datetime_object.strftime("%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise ValidationError(f"{self.name} invalid date format YYY-MM-DD or YYY-MM-DD HH:MM:SS required")


class BooleanFilter(BaseFilter):
    def __init__(self, **kwargs):
        self.filter_required = kwargs.pop('required')
        super().__init__(**kwargs)

    def clean(self, value):
        if not value.strip() and self.filter_required:
            raise ValidationError(f"{self.name} cannot be empty")
        return string_to_bool(value.strip())


class ArrayFilter(BaseFilter):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def clean(self, value):
        return map(self.cast, value.split(','))
