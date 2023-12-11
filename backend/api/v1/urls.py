from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from api.v1.views import CategoryViewSet, SubcategoryViewSet

router = DefaultRouter()

ROUTER_DATA: list[dict[str, ModelViewSet]] = [
    {'prefix': 'categories', 'viewset': CategoryViewSet},
    {'prefix': 'subcategories', 'viewset': SubcategoryViewSet},
]

for route in ROUTER_DATA:
    router.register(
        prefix=route.get('prefix'),
        viewset=route.get('viewset'),
        basename=route.get('prefix'),
    )

urlpatterns = [
    path('', include(router.urls)),
]