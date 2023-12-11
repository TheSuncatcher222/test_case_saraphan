from rest_framework.viewsets import ModelViewSet

from api.v1.serializers import (
    CategoryGetSerializer, SubcategoryGetSerializer,
)
from goods.models import Category, Good, ShoppingCart, Subcategory


class CategoryViewSet(ModelViewSet):
    """Вью-сет для взаимодействия с моделью Category."""

    http_method_names = ('get',)
    serializer_class = CategoryGetSerializer
    queryset = Category.objects.all()


class SubcategoryViewSet(ModelViewSet):
    """Вью-сет для взаимодействия с моделью Subcategory."""

    http_method_names = ('get',)
    serializer_class = SubcategoryGetSerializer
    queryset = Subcategory.objects.all().select_related('category')
