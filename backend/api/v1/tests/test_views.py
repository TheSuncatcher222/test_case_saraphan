from typing import OrderedDict

import pytest
from rest_framework.test import APIClient

from api.v1.tests.conftest import (
    URL_STATUS_200, URL_STATUS_201, URL_STATUS_204,
    URL_AUTH_CREATE, URL_AUTH_REFRESH, URL_CATEGORIES, URL_CREATE_NUMS_ROW,
    URL_GOODS, URL_SHOPPING_CART, URL_SHOPPING_CART_CLEAR, URL_SUBCATEGORIES,
    client_anon, client_auth,
)


@pytest.mark.django_db
class TestEndpoints():
    """
    Производит тест функционала эндпоинтов в urlpatterns.
    """

    @pytest.mark.parametrize(
        'num, status, expected', (
            (
                5,
                URL_STATUS_200,
                {'number_sequence': '122333444455555'}
            ),
            (
                2,
                URL_STATUS_200,
                {'number_sequence': '122'}
            ),
        )
    )
    def test_create_nums_row(self, num, status, expected) -> None:
        """Тестирует POST запрос на генерацию числовой последовательности."""
        response = client_anon().post(
            path=URL_CREATE_NUMS_ROW,
            data={"number": num},
            format='json',
        )
        assert response.status_code == status
        assert response.data == expected
        return

    def test_get_jwt_tokens(self, create_users) -> None:
        """
        Тест POST запроса на получение пары JWT-токенов доступа и обновления.
        """
        response = client_anon().post(
            path=URL_AUTH_CREATE,
            data={
                "username": 'user_1',
                "password": '!user_PASSWORD_1!'
            },
            format='json',
        )
        assert response.status_code == URL_STATUS_200
        access_token = response.data.get('access')
        refresh_token = response.data.get('refresh')
        missed_tokens: list[str] = []
        for token in (access_token, refresh_token):
            if token is None:
                missed_tokens.append(token)
        assert not missed_tokens, (
            f'Убедитесь, что эндпоинт {URL_AUTH_CREATE} возвращает '
            f'токен(ы): {", ".join(token for token in missed_tokens)}.'
        )
        response = client_anon().post(
            path=URL_AUTH_REFRESH,
            data={
                "refresh": refresh_token
            },
            format='json',
        )
        assert response.status_code == URL_STATUS_200
        access_token = response.data.get('access')
        assert access_token is not None, (
            f'Убедитесь, что эндпоинт {URL_AUTH_REFRESH} обновляет '
            'токен доступа.'
        )
        return

    def test_get_categories(self, create_staff) -> None:
        """
        Тест GET запроса на получение списка категорий товаров.
        """
        response = client_anon().get(
            path=URL_CATEGORIES,
        )
        assert response.status_code == URL_STATUS_200
        assert list(response.data.keys()) == ['count', 'next', 'previous', 'results'], (  # noqa (E501)
            f'Убедитесь, что эндпоинт {URL_CATEGORIES} содержит пагинацию.'
        )
        assert response.data['results'] == [
            OrderedDict(
                [
                    ('id', 1),
                    ('name', 'Категория 1'),
                    ('slug', 'category-1'),
                    ('image', None)
                ]
            ),
            OrderedDict(
                [
                    ('id', 2),
                    ('name', 'Категория 2'),
                    ('slug', 'category-2'),
                    ('image', None)
                ]
            ),
            OrderedDict(
                [
                    ('id', 3),
                    ('name', 'Категория 3'),
                    ('slug', 'category-3'),
                    ('image', None)
                ]
            )
        ], (
            f'Убедитесь, что эндпоинт {URL_CATEGORIES} '
            'выводит информацию о категориях товаров.'
        )
        return

    def test_get_goods(self, create_staff) -> None:
        """
        Тест GET запроса на получение списка товаров.
        """
        response = client_anon().get(
            path=URL_GOODS,
        )
        assert response.status_code == URL_STATUS_200
        assert list(response.data.keys()) == ['count', 'next', 'previous', 'results'], (  # noqa (E501)
            f'Убедитесь, что эндпоинт {URL_GOODS} содержит пагинацию.'
        )
        assert response.data['results'] == [
            OrderedDict(
                [
                    ('id', 1),
                    ('name', 'Товар 1'),
                    ('slug', 'good-1'),
                    ('price', 1),
                    (
                        'subcategory',
                        OrderedDict(
                            [
                                ('id', 1),
                                ('name', 'Подкатегория 1'),
                                ('slug', 'subcategory-1'),
                                ('parent_category', 'Категория 1')
                            ]
                        )
                    ),
                    ('image_large', None),
                    ('image_medium', None),
                    ('image_small', None)
                ]
            ),
            OrderedDict(
                [
                    ('id', 2),
                    ('name', 'Товар 2'),
                    ('slug', 'good-2'),
                    ('price', 2),
                    (
                        'subcategory',
                        OrderedDict(
                            [
                                ('id', 2),
                                ('name', 'Подкатегория 2'),
                                ('slug', 'subcategory-2'),
                                ('parent_category', 'Категория 2')
                            ]
                        )
                    ),
                    ('image_large', None),
                    ('image_medium', None),
                    ('image_small', None)
                ]
            ),
            OrderedDict(
                [
                    ('id', 3),
                    ('name', 'Товар 3'),
                    ('slug', 'good-3'),
                    ('price', 3),
                    (
                        'subcategory',
                        OrderedDict(
                            [
                                ('id', 3),
                                ('name', 'Подкатегория 3'),
                                ('slug', 'subcategory-3'),
                                ('parent_category', 'Категория 3')
                            ]
                        )
                    ),
                    ('image_large', None),
                    ('image_medium', None),
                    ('image_small', None)
                ]
            )
        ], (
            f'Убедитесь, что эндпоинт {URL_GOODS} '
            'выводит информацию о товарах.'
        )
        return

    def test_shopping_cart(self, create_staff) -> None:
        """
        Тест GET запроса на получение списка подкатегорий товаров.
        """
        client: APIClient = client_auth()
        response = client.get(
            path=URL_SHOPPING_CART,
        )
        assert response.status_code == URL_STATUS_200
        assert list(response.data.keys()) == ['total_goods', 'total_sum', 'goods'], (  # noqa (E501)
            f'Убедитесь, что эндпоинт {URL_SHOPPING_CART} содержит информацию '
            'об общем количестве товаров (total_goods), общей цене товаров '
            '(total_sum) и список товаров (goods).'
        )
        assert response.data['goods'] == [], (
            'Убедитесь, что нет активных фикстур наполнения корзины пользователя.'  # noqa (E501)
        )
        response = client.post(
            path=URL_SHOPPING_CART,
            data={
                "goods": [
                    {
                        "good": 1,
                        "amount": 10
                    },
                    {
                        "good": 2,
                        "amount": 20
                    }
                ]
            },
            format='json',
        )
        assert response.status_code == URL_STATUS_201
        assert response.data == {
            'total_goods': 2,
            'total_sum': 50,
            'goods': [
                {
                    'good': 'Товар 1',
                    'price': 1,
                    'amount': 10
                },
                {
                    'good': 'Товар 2',
                    'price': 2,
                    'amount': 20
                }
            ]
        }, ('Убедитесь, что добавление товаров в корзину работает корректно.')
        response = client.post(
            path=URL_SHOPPING_CART,
            data={
                "goods": [
                    {
                        "good": 1,
                        "amount": 20
                    },
                    {
                        "good": 3,
                        "amount": 10
                    }
                ]
            },
            format='json',
        )
        assert response.status_code == URL_STATUS_201
        assert response.data == {
            'total_goods': 2,
            'total_sum': 50,
            'goods': [
                {
                    'good': 'Товар 1',
                    'price': 1,
                    'amount': 20
                },
                {
                    'good': 'Товар 3',
                    'price': 3,
                    'amount': 10
                }
            ]
        }, ('Убедитесь, что обновление товаров в корзине работает корректно.')
        response = client.post(
            path=URL_SHOPPING_CART_CLEAR,
        )
        assert response.status_code == URL_STATUS_204
        response = client.get(
            path=URL_SHOPPING_CART,
        )
        assert response.status_code == URL_STATUS_200
        assert response.data['goods'] == [], (
            'Убедитесь, что очистка корзины работает корректно.'
        )
        return

    def test_get_subcategories(self, create_staff) -> None:
        """
        Тест GET запроса на получение списка подкатегорий товаров.
        """
        response = client_anon().get(
            path=URL_SUBCATEGORIES,
        )
        assert response.status_code == URL_STATUS_200
        assert list(response.data.keys()) == ['count', 'next', 'previous', 'results'], (  # noqa (E501)
            f'Убедитесь, что эндпоинт {URL_SUBCATEGORIES} содержит пагинацию.'
        )
        assert response.data['results'] == [
            OrderedDict(
                [
                    ('id', 1),
                    ('name', 'Подкатегория 1'),
                    ('slug', 'subcategory-1'),
                    (
                        'category',
                        OrderedDict(
                            [
                                ('id', 1),
                                ('name', 'Категория 1'),
                                ('slug', 'category-1'),
                                ('image', None)
                            ]
                        )
                    ),
                    ('image', None)
                ]
            ),
            OrderedDict(
                [
                    ('id', 2),
                    ('name', 'Подкатегория 2'),
                    ('slug', 'subcategory-2'),
                    (
                        'category',
                        OrderedDict(
                            [
                                ('id', 2),
                                ('name', 'Категория 2'),
                                ('slug', 'category-2'),
                                ('image', None)
                            ]
                        )
                    ),
                    ('image', None)
                ]
            ),
            OrderedDict(
                [
                    ('id', 3),
                    ('name', 'Подкатегория 3'),
                    ('slug', 'subcategory-3'),
                    (
                        'category',
                        OrderedDict(
                            [
                                ('id', 3),
                                ('name', 'Категория 3'),
                                ('slug', 'category-3'),
                                ('image', None)
                            ]
                        )
                    ),
                    ('image', None)
                ]
            )
        ], (
            f'Убедитесь, что эндпоинт {URL_CATEGORIES} '
            'выводит информацию о подкатегориях товаров.'
        )
        return
