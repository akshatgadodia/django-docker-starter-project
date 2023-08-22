from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from common import constants

swagger_view = get_schema_view(
   openapi.Info(
      title=constants.TITLE,
      default_version=constants.CURRENT_VERSION,
      description=constants.DESCRIPTION,
      terms_of_service=constants.TERMS_URL,
      contact=openapi.Contact(email=constants.CONTACT_EMAIL),
      license=openapi.License(name=constants.PROJECT_LICENSE_NAME),
   ),
   public=True,
   permission_classes=(AllowAny,),
)
