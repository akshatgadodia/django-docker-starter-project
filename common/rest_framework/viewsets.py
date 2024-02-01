from rest_framework import viewsets, status, serializers, filters

from common.rest_framework.filters import QueryFilterBackend
from common.rest_framework.mixins import APIViewResponseMixin
from common.rest_framework.pagination import StandardResultsSetPagination
from common.rest_framework.utils import get_object_or_404
from common.rest_framework import messages
from vendors.utils import vendor_filter


class BaseViewSet(viewsets.ModelViewSet, APIViewResponseMixin):
    """
    Base ViewSet for Django Rest Framework with extended functionality.

    This ViewSet provides common features such as authentication, response handling, and default behaviors
    for CRUD operations. It extends the Django Rest Framework's ModelViewSet and includes additional
    mixins for API response customization.

    Attributes:
        model (class): The Django model associated with this ViewSet.
        queryset (QuerySet): The base queryset used for retrieving objects.
        pagination_class (class): The pagination class to use for list views.
        serializer_class (class): The default serializer class for the ViewSet.
        serializer_classes (dict): A dictionary mapping action names to serializer classes.
        default_messages (dict): A dictionary containing default success/failure messages for various actions.
        messages (dict): Additional or overridden messages for specific actions.
        api_permissions (dict): API Permissions for the different actions

    Methods:
        get_permissions: Returns a list of permission classes for the ViewSet.
        get_message: Retrieves a message for a specific action, using custom or default messages.
        get_serializer_class: Returns the serializer class based on the current action.
        create: Handles object creation and returns a success or failure response.
        retrieve: Retrieves a single object and returns a serialized response.
        update: Updates an existing object and returns a success or failure response.
        destroy: Deletes an object and returns a success or failure response.
        list: Retrieves a paginated list of objects and returns a serialized response.
    """
    model = None
    model_name = None
    queryset = None
    filter_backends = (QueryFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    pagination_class = StandardResultsSetPagination
    serializer_class = serializers.Serializer
    serializer_classes = {
        'create': None,
        'retrieve': None,
        'list': None,
        'update': None,
        'destroy': None,
    }
    default_messages = {
        'create_success': messages.CREATE_SUCCESS_MESSAGE,
        'create_failure': messages.INVALID_DATA,
        'retrieve_failure': messages.RETRIEVE_FAILURE_MESSAGE,
        'destroy_success': messages.DESTROY_SUCCESS_MESSAGE,
        'destroy_failure': messages.DESTROY_FAILURE_MESSAGE,
        'update_success': messages.UPDATE_SUCCESS_MESSAGE,
        'update_failure': messages.UPDATE_FAILURE_MESSAGE
    }
    messages = {}
    api_permissions = {}
    query_filters = []
    search_fields = []
    ordering_fields = []

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = vendor_filter(queryset=queryset)
        return queryset

    def get_serializer_context(self):
        """
        Override this method to pass the request object as context to the serializer.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def get_message(self, key):
        """
        Retrieve a message for a specific action.
        This method looks for a custom message in the `messages` dictionary for the given key.
        If a custom message is not found, it uses the default message from the `default_messages`
        dictionary, substituting the model description if available.
        """
        message = self.messages.get(key)
        if message:
            return message
        model_description = 'Resource'
        if self.model_name:
            model_description = self.model_name
        elif self.model and self.model._meta.verbose_name:
            model_description = self.model._meta.verbose_name
        default_message = self.default_messages.get(key, '').format(model=model_description)
        return default_message

    def get_serializer_class(self):
        """
        Get the serializer class based on the current action.
        This method retrieves the serializer class from the `serializer_classes` dictionary
        based on the current action. If a specific serializer is not defined for the action,
        it returns the default serializer class.
        """
        serializer = self.serializer_classes.get(self.action)
        return self.serializer_class if serializer is None else serializer

    def create(self, request, *args, **kwargs):
        """
        Handle object creation and return a success or failure response.
        This method creates a new object using the provided data and validates the serializer.
        If the serializer is valid, the `perform_create` method is called, and a success response
        is returned. If the serializer is not valid, a failure response is returned with details
        about the validation errors.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return self.success_response(status_code=status.HTTP_201_CREATED,
                                         message=self.get_message('create_success'))
        else:
            non_field_errors = serializer.errors.get('non_field_errors', [])
            message = non_field_errors[0] if non_field_errors else self.get_message('create_failure')
            return self.failure_response(data=serializer.errors, message=message,
                                         status_code=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a single object and return a serialized response.
        This method retrieves an object with the specified primary key and serializes it.
        If the object is an instance of the specified model, a success response containing
        the serialized data is returned. If the object is not found or does not match the
        expected model, an appropriate error response is returned.
        """
        pk = kwargs.get('pk')
        get_object_status, instance = get_object_or_404(queryset=self.get_queryset(),
                                                        error_message=self.get_message('retrieve_failure'),
                                                        id=pk)
        if get_object_status:
            serializer = self.get_serializer(instance)
            return self.success_response(data=serializer.data, status_code=status.HTTP_200_OK)
        return self.failure_response(message=instance, status_code=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        """
        Update an existing object and return a success or failure response.
        This method retrieves an object with the specified primary key, validates the provided
        data using the serializer, and updates the object if the data is valid. If the update is
        successful, a success response is returned. If the data is not valid or the object is not
        found, a failure response with details about the errors is returned.
        """
        pk = kwargs.get('pk')
        partial = kwargs.pop('partial', False)
        get_object_status, instance = get_object_or_404(queryset=self.get_queryset(),
                                                        error_message=self.get_message('retrieve_failure'),
                                                        id=pk)
        if get_object_status:
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            if serializer.is_valid():
                self.perform_update(serializer)
                return self.success_response(message=self.get_message('update_success'),
                                             status_code=status.HTTP_200_OK)
            else:
                return self.failure_response(data=serializer.errors, message=self.get_message('update_failure'),
                                             status_code=status.HTTP_400_BAD_REQUEST)
        return self.failure_response(message=instance, status_code=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an object and return a success or failure response.
        This method retrieves an object with the specified primary key and deletes it.
        If the deletion is successful, a success response is returned. If the object is not
        found, a failure response is returned.
        """
        pk = kwargs.get('pk')
        get_object_status, instance = get_object_or_404(queryset=self.get_queryset(),
                                                        error_message=self.get_message('retrieve_failure'),
                                                        id=pk)
        if get_object_status:
            self.perform_destroy(instance)
            return self.success_response(message=self.get_message('destroy_success'),
                                         status_code=status.HTTP_200_OK)
        return self.failure_response(message=instance, status_code=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        """
        Retrieve a paginated list of objects and return a serialized response.
        This method filters the queryset based on the request, paginates the results,
        and returns a success response containing the paginated list of serialized data.
        """
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        data = self.get_paginated_response(serializer.data)
        return self.success_response(data=data, status_code=status.HTTP_200_OK)
