from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from api.v1.views import (
    CategoryViewSet, CustomTokenObtainPairView, CustomTokenRefreshView,
    GoodViewSet, ShoppingCartViewSet, SubcategoryViewSet,
    create_nums_row,
)

router = DefaultRouter()

ROUTER_DATA: list[dict[str, ModelViewSet]] = [
    {'prefix': 'categories', 'viewset': CategoryViewSet},
    {'prefix': 'goods', 'viewset': GoodViewSet},
    {'prefix': 'shopping-cart', 'viewset': ShoppingCartViewSet},
    {'prefix': 'subcategories', 'viewset': SubcategoryViewSet},
]

urlpatterns_token = [
    path('create/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
]

for route in ROUTER_DATA:
    router.register(
        prefix=route.get('prefix'),
        viewset=route.get('viewset'),
        basename=route.get('prefix'),
    )

urlpatterns = [
    path('', include(router.urls)),
    path('create-nums-row/', create_nums_row),
    path('auth/token/', include(urlpatterns_token)),
]
