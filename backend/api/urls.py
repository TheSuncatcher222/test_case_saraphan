from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView,
)

from api.v1.urls import urlpatterns as urlpatterns_v1


urlpatterns_schema = [
    path('', SpectacularAPIView.as_view(), name='schema'),
    path('swagger-ui/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(), name='redoc'),
]

urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
    path('schema/', include(urlpatterns_schema)),
]
