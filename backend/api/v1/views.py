from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView,
)

from api.v1.schemas import (
    CATEGORIES_VIEW_SCHEMA, GOODS_VIEW_SCHEMA,
    SHOPPING_CART_SCHEMA, SUBCATEGORIES_VIEW_SCHEMA,
    TOKEN_JWT_OBTAIN_SCHEMA, TOKEN_JWT_REFRESH_SCHEMA,
)
from api.v1.serializers import (
    CategoryGetSerializer, GoodGetSerializer,
    NumberSerializer,
    ShoppingCartGetSerializer, ShoppingCartPostListSerializer,
    SubcategoryGetSerializer,
)
from goods.models import Category, Good, ShoppingCart, Subcategory


# INFO: выбран метод POST, так как он точно не будет закеширован
#       ни на сервере, ни на клиенте.
@api_view(http_method_names=('POST',))
def create_nums_row(request):
    """
    Функция, которая выводит n первых элементов последовательности
    122333444455555… (число повторяется столько раз, чему оно равно).
    """
    serializer = NumberSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    number: int = serializer.validated_data['number']
    arith_progress: int = sum(i for i in range(number+1))
    nums: list[int] = [None] * arith_progress
    point: int = 0
    for i in range(number+1):
        j: int = 0
        for j in range(i):
            nums[point] = i
            point += 1
            j += 1
    data: dict[str, str] = {
        "number_sequence": ''.join(map(str, nums))
    }
    return Response(
        status=status.HTTP_200_OK,
        data=data,
    )


@extend_schema(**TOKEN_JWT_OBTAIN_SCHEMA)
class CustomTokenObtainPairView(TokenObtainPairView):
    """Используется для обновления swagger к эндпоинту получения токенов."""
    pass


@extend_schema(**TOKEN_JWT_REFRESH_SCHEMA)
class CustomTokenRefreshView(TokenRefreshView):
    """Используется для обновления swagger к эндпоинту обновления токена."""
    pass


@extend_schema_view(**CATEGORIES_VIEW_SCHEMA)
class CategoryViewSet(ModelViewSet):
    """Вью-сет для взаимодействия с моделью Category."""

    http_method_names = ('get',)
    serializer_class = CategoryGetSerializer
    queryset = Category.objects.all()


@extend_schema_view(**GOODS_VIEW_SCHEMA)
class GoodViewSet(ModelViewSet):
    """Вью-сет для взаимодействия с моделью Good."""

    http_method_names = ('get',)
    serializer_class = GoodGetSerializer
    queryset = Good.objects.all().select_related('subcategory')


@extend_schema_view(**SHOPPING_CART_SCHEMA)
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

    @extend_schema(exclude=True,)
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


@extend_schema_view(**SUBCATEGORIES_VIEW_SCHEMA)
class SubcategoryViewSet(ModelViewSet):
    """Вью-сет для взаимодействия с моделью Subcategory."""

    http_method_names = ('get',)
    serializer_class = SubcategoryGetSerializer
    queryset = Subcategory.objects.all().select_related('category')
