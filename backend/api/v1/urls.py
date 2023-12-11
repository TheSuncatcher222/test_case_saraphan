from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

from api.v1.views import (
    CategoryViewSet, GoodViewSet, ShoppingCartViewSet, SubcategoryViewSet,
)

router = DefaultRouter()

ROUTER_DATA: list[dict[str, ModelViewSet]] = [
    {'prefix': 'categories', 'viewset': CategoryViewSet},
    {'prefix': 'goods', 'viewset': GoodViewSet},
    {'prefix': 'shopping-cart', 'viewset': ShoppingCartViewSet},
    {'prefix': 'subcategories', 'viewset': SubcategoryViewSet},
]

urlpatterns_token = [
    path('create/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

for route in ROUTER_DATA:
    router.register(
        prefix=route.get('prefix'),
        viewset=route.get('viewset'),
        basename=route.get('prefix'),
    )

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', include(urlpatterns_token)),
]
