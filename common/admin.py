from django.contrib import admin
from django.urls import re_path
from django.http import HttpResponseRedirect
from django.utils.encoding import force_str
from django.utils.translation import gettext as _

from common.constants import DEFAULT_SINGLETON_INSTANCE_ID


class BaseModelAdmin(admin.ModelAdmin):
    """
    Base class for model admins with common functionality.
    Attributes:
        empty_value_display (str): Display value for empty fields.
        show_full_result_count (bool): Flag to show the full result count.
    """

    # Default options for all model admins
    empty_value_display = ''
    show_full_result_count = False
    exclude = ('created_at', 'updated_at', 'created_by', 'updated_by', 'deleted_at', 'deleted_by')

    def save_model(self, request, obj, form, change):
        """
        Override the default save_model method to set created_by and updated_by fields.
        Args:
            request (HttpRequest): The incoming request.
            obj: The object being saved.
            form: The form used to save the object.
            change (bool): Flag indicating if the object is being edited.
        Returns:
            None
        """
        user = request.user
        if change:
            obj.updated_by = user
        else:
            obj.created_by = user
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """
        Override the default delete_model method to soft delete the object.
        Args:
            request (HttpRequest): The incoming request.
            obj: The object being deleted.
        Returns:
            None
        """
        obj.delete(user=request.user)

    def delete_queryset(self, request, queryset):
        """
        Override the default delete_queryset method to soft delete the queryset.
        Args:
            request (HttpRequest): The incoming request.
            queryset: The queryset being deleted.
        Returns:
            None
        """
        queryset.delete()


class SingletonModelAdmin(BaseModelAdmin):
    """
    Model admin for singleton models.
    Attributes:
        singleton_instance_id (int): The ID of the singleton instance.
    """

    def has_add_permission(self, request):
        """
        Override the default has_add_permission method to disallow adding new instances.
        Args:
            request (HttpRequest): The incoming request.
        Returns:
            bool: False to disallow adding new instances.
        """
        return False

    def has_delete_permission(self, request, obj=None):
        """
        Override the default has_delete_permission method to disallow deleting instances.
        Args:
            request (HttpRequest): The incoming request.
            obj: The object being deleted (ignored).
        Returns:
            bool: False to disallow deleting instances.
        """
        return False

    def get_urls(self):
        """
        Override the default get_urls method to include custom URLs for change and history views.
        Returns:
            list: Custom URLs along with the default URLs.
        """
        urls = super(SingletonModelAdmin, self).get_urls()
        model_name = self.model._meta.model_name

        url_name_prefix = '%(app_name)s_%(model_name)s' % {
            'app_name': self.model._meta.app_label,
            'model_name': model_name,
        }
        custom_urls = [
            re_path(r'^history/$',
                    self.admin_site.admin_view(self.history_view),
                    {'object_id': str(self.singleton_instance_id)},
                    name='%s_history' % url_name_prefix),
            re_path(r'^$',
                    self.admin_site.admin_view(self.change_view),
                    {'object_id': str(self.singleton_instance_id)},
                    name='%s_change' % url_name_prefix),
        ]

        return custom_urls + urls

    def response_change(self, request, obj):
        """
        Override the default response_change method to redirect to the home page after a successful change.
        Args:
            request (HttpRequest): The incoming request.
            obj: The object being changed.
        Returns:
            HttpResponseRedirect: Redirect to the home page.
        """
        msg = _('%(obj)s was changed successfully.') % {'obj': force_str(obj)}
        if '_continue' in request.POST:
            # Continue editing the object
            self.message_user(request, msg + ' ' + _('You may edit it again below.'))
            return HttpResponseRedirect(request.path)
        else:
            # Redirect to the home page after successful change
            self.message_user(request, msg)
            return HttpResponseRedirect("../../")

    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Override the default change_view method to display the change form for the default singleton instance ID.
        Args:
            request (HttpRequest): The incoming request.
            object_id: The object ID (ignored).
            form_url: The form URL (ignored).
            extra_context: Additional context for the template.
        Returns:
            HttpResponse: The response containing the change form.
        """
        if object_id == str(self.singleton_instance_id):
            # Create the singleton instance if it doesn't exist
            self.model.objects.get_or_create(pk=self.singleton_instance_id)

        if not extra_context:
            extra_context = dict()
        extra_context['skip_object_list_page'] = True

        return super(SingletonModelAdmin, self).change_view(
            request,
            object_id,
            form_url=form_url,
            extra_context=extra_context,
        )

    def history_view(self, request, object_id, extra_context=None):
        """
        Override the default history_view method to display the history of the default singleton instance ID.
        Args:
            request (HttpRequest): The incoming request.
            object_id: The object ID (ignored).
            extra_context: Additional context for the template.
        Returns:
            HttpResponse: The response containing the object history.
        """
        if not extra_context:
            extra_context = dict()
        extra_context['skip_object_list_page'] = True

        return super(SingletonModelAdmin, self).history_view(
            request,
            object_id,
            extra_context=extra_context,
        )

    @property
    def singleton_instance_id(self):
        """
        Get the singleton instance ID from the model, defaulting to DEFAULT_SINGLETON_INSTANCE
        """
        # Get the singleton instance id from the model, defaulting to DEFAULT_SINGLETON_INSTANCE_ID
        return getattr(self.model, 'singleton_instance_id', DEFAULT_SINGLETON_INSTANCE_ID)

