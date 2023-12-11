from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer, TokenRefreshSerializer,
)
from api.v1.serializers import ShoppingCartGetSerializer

DEFAULT_400_REQUIRED: str = 'Обязательное поле.'
DEFAULT_401: str = 'Учетные данные не были предоставлены.'
DEFAULT_404: str = 'Страница не найдена.'


class ShoppingCartListSerializer(serializers.Serializer):

    total_goods = serializers.IntegerField()
    total_sum = serializers.IntegerField()
    goods = ShoppingCartGetSerializer()

    class Meta:
        fields = (
            'total_goods',
            'total_sum',
            'goods',
        )


CATEGORIES_VIEW_SCHEMA: dict[str, str] = {
    'list': extend_schema(
        description=(
            'Возвращает список категорий товаров.'
        ),
        summary='Получить список категорий товаров.',
    ),
    'retrieve': extend_schema(
        description=(
            'Возвращает категорию товара с указанным идентификатором.'
        ),
        summary='Получить категорию товара.',
    ),
}

GOODS_VIEW_SCHEMA: dict[str, str] = {
    'list': extend_schema(
        description=(
            'Возвращает список товаров.'
        ),
        summary='Получить список товаров.',
    ),
    'retrieve': extend_schema(
        description=(
            'Возвращает товар с указанным идентификатором.'
        ),
        summary='Получить товар.',
    ),
}

SHOPPING_CART_SCHEMA = {
    'list': extend_schema(
        description='Возвращает список товаров в корзине с покупками.',
        summary='Получить список товаров в корзине с покупками.',
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='shopping_cart_get_200',
                fields={
                    'total_goods': serializers.IntegerField(),
                    'total_sum': serializers.IntegerField(),
                    'goods': ShoppingCartGetSerializer(),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='clear_shopping_cart_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
        },
    ),
    'create': extend_schema(
        description='Обновляет список товаров в корзине с покупками.',
        summary='Обновить список товаров в корзине с покупками.',
        request=inline_serializer(
            name='shopping_cart_create_201',
                fields={
                    'goods': ShoppingCartGetSerializer(),
                },
        ),
        responses={
            status.HTTP_200_OK: inline_serializer(
                name='shopping_cart_get_200',
                fields={
                    'total_goods': serializers.IntegerField(),
                    'total_sum': serializers.IntegerField(),
                    'goods': ShoppingCartGetSerializer(),
                },
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='clear_shopping_cart_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
        },
    ),
    'clear_shopping_cart': extend_schema(
        description=(
            'Очищает список товаров в корзине с покупками.'
        ),
        summary='Очистить список товаров в корзине с покупками.',
        request=None,
        responses={
            status.HTTP_204_NO_CONTENT: inline_serializer(
                name='clear_shopping_cart_answer_200',
                fields={},
            ),
            status.HTTP_401_UNAUTHORIZED: inline_serializer(
                name='clear_shopping_cart_error_401',
                fields={
                    'detail': serializers.CharField(
                        default=DEFAULT_401,
                    ),
                },
            ),
        },
    ),
}

SUBCATEGORIES_VIEW_SCHEMA: dict[str, str] = {
    'list': extend_schema(
        description=(
            'Возвращает список подкатегорий товаров.'
        ),
        summary='Получить список подкатегорий товаров.',
    ),
    'retrieve': extend_schema(
        description=(
            'Возвращает подкатегорию товара с указанным идентификатором.'
        ),
        summary='Получить подкатегорию товара.',
    ),
}

TOKEN_JWT_OBTAIN_SCHEMA: dict[str, str] = {
    'description': (
        'Принимает набор учетных данных пользователя и возвращает '
        'пару JWT-токенов доступа и обновления.'
    ),
    'summary': 'Получить пару JWT-токенов доступа и обновления.',
    'responses': {
        status.HTTP_200_OK: TokenObtainPairSerializer,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='token_pair_create_error_400',
            fields={
                'detail': serializers.CharField(
                    default=(
                        'No active account found with the given credentials'
                    ),
                ),
            },
        ),
    },
}

TOKEN_JWT_REFRESH_SCHEMA: dict[str, str] = {
    'description': (
        'Принимает JWT-токен обновления и возвращает JWT-токен доступа, '
        'если токен обновления действителен.'
    ),
    'summary': 'Обновить JWT-токен доступа.',
    'responses': {
        status.HTTP_200_OK: TokenRefreshSerializer,
        status.HTTP_400_BAD_REQUEST: inline_serializer(
            name='access_token_refresh_error_400',
            fields={
                'detail': serializers.CharField(
                    default='Token is invalid or expired',
                ),
                'code': serializers.CharField(
                    default='token_not_valid',
                ),
            },
        ),
    },
}
