from django.urls import include, path

from api.v1.urls import urlpatterns as urlpatterns_v1

urlpatterns = [
    path('v1/', include(urlpatterns_v1)),
]
