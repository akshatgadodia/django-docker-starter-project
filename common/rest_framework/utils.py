from rest_framework.status import HTTP_200_OK
from django.http import JsonResponse

from common.constants import FAILED
from common.services.threadlocals import thread_local


def get_object_or_404(queryset=None, error_message=None, **kwargs):
    """
    Use get() to return an object, or send failure response if the object does not exist.
    """
    try:
        kwargs['vendor'] = thread_local.get_vendor()
        return True, queryset.get(**kwargs)
    except queryset.model.DoesNotExist:
        if error_message is None:
            error_message = f"{queryset.model._meta.object_name} not found"
    return False, error_message


def send_json_response(message=None, data=None, status=FAILED, status_code=HTTP_200_OK):
    response_data = {
        "status": status,
        "status_code": status_code,
        "data": {
            **({"message": message} if message is not None else {}),
            **({"data": data} if not isinstance(data, dict) else data)
        }
    }
    return JsonResponse(response_data, status=status_code)
