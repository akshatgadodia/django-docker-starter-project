from rest_framework import permissions
from rest_framework.exceptions import NotAuthenticated

from common.messages import USER_NOT_AUTHENTICATED


class ApiPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        api_permissions = getattr(view, 'api_permissions', None)
        module = getattr(view, 'module', view.__module__.split('.')[0])

        if api_permissions:
            method_permissions = api_permissions.get(request.method.lower(), None)
            if method_permissions:
                return any([request.user.has_perm(permission if "." in permission else f"{module}.{permission}")
                            for permission in method_permissions])
            else:
                return True
        else:
            raise AssertionError("api_permission should be set to use ApiPermission Class")
