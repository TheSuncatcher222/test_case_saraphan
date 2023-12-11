from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.serializers import (
    CategoryGetSerializer, GoodGetSerializer,
    ShoppingCartGetSerializer, ShoppingCartPostListSerializer,
    SubcategoryGetSerializer,
)
from goods.models import Category, Good, ShoppingCart, Subcategory


class CategoryViewSet(ModelViewSet):
    """Вью-сет для взаимодействия с моделью Category."""

    http_method_names = ('get',)
    serializer_class = CategoryGetSerializer
    queryset = Category.objects.all()


class GoodViewSet(ModelViewSet):
    """Вью-сет для взаимодействия с моделью Good."""

    http_method_names = ('get',)
    serializer_class = GoodGetSerializer
    queryset = Good.objects.all().select_related('subcategory')


class ShoppingCartViewSet(ModelViewSet):
    """Вью-сет для взаимодействия с моделью ShoppingCart."""

    http_method_names = ('get', 'post',)
    permission_classes = (IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return ShoppingCart.objects.filter(
            user=self.request.user,
        ).select_related(
            'user',
            'good'
        )

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ShoppingCartGetSerializer
        return ShoppingCartPostListSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        data: dict[str, any] = serializer.data
        total_goods: int = len(data)
        total_sum: int = sum(
            item.get('price', 0) * item.get('amount', 0) for item in data
        )
        return Response(
            data={
                'total_goods': total_goods,
                'total_sum': total_sum,
                'goods': data
            },
            status=status.HTTP_200_OK,
        )

    def create(self, request, *args, **kwargs):
        data: dict[str, any] = request.data
        data['user'] = self.request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ShoppingCart.objects.filter(user=self.request.user).delete()
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(
        methods=('post',),
        detail=False,
        url_name='clear-shopping-cart',
    )
    def clear_shopping_cart(self, request):
        """Очищает пользовательскую корзину с покупками."""
        ShoppingCart.objects.filter(user=request.user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubcategoryViewSet(ModelViewSet):
    """Вью-сет для взаимодействия с моделью Subcategory."""

    http_method_names = ('get',)
    serializer_class = SubcategoryGetSerializer
    queryset = Subcategory.objects.all().select_related('category')
