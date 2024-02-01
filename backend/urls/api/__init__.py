from django.urls import path, include

urlpatterns = [
    path('v1/', include('backend.urls.api.v1'))
]
