from django.urls import path, include
from common.rest_framework.swagger import swagger_view

urlpatterns = [
    path('users/', include('users.api.v1.urls')),
    path('docs/', swagger_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
