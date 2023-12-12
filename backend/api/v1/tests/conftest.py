import pytest

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from goods.models import Category, Good, Subcategory


"""API клиенты."""


def client_anon() -> APIClient:
    """Возвращает объект анонимного клиента."""
    return APIClient()


def client_auth() -> APIClient:
    """Возвращает объект анонимного клиента."""
    user, created = User.objects.get_or_create(
        username='auth_user',
        email='auth_user@email.com',
    )
    if created:
        user.set_password('testpassword')
        user.save()
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return client


"""Статусы запросов."""


# INFO: список статусов, которые может вернуть сервер,
#       если эндпоинт не доступен по указанному адресу.
URL_MISSED_STATUSES: list = [
    status.HTTP_301_MOVED_PERMANENTLY,
    status.HTTP_302_FOUND,
    status.HTTP_303_SEE_OTHER,
    status.HTTP_307_TEMPORARY_REDIRECT,
    status.HTTP_308_PERMANENT_REDIRECT,
    status.HTTP_404_NOT_FOUND,
    status.HTTP_408_REQUEST_TIMEOUT,
    status.HTTP_409_CONFLICT,
    status.HTTP_410_GONE,
]

URL_STATUS_200 = status.HTTP_200_OK
URL_STATUS_201 = status.HTTP_201_CREATED
URL_STATUS_204 = status.HTTP_204_NO_CONTENT
URL_STATUS_400 = status.HTTP_400_BAD_REQUEST


"""Фикстуры."""


# Количество объектов моделей, должны создавать все фикстуры.
TEST_FIXTURES_OBJ_AMOUNT: int = 3


def create_user_obj(num: int):
    user: User = User.objects.create(
        username=f'user_{num}',
        email=f'user_{num}@email.com',
    )
    user.set_password(f'!user_PASSWORD_{num}!')
    user.save()
    return


@pytest.fixture()
def create_users() -> None:
    """Фикстура для наполнения БД заданным числом пользователей."""
    for i in range(1, TEST_FIXTURES_OBJ_AMOUNT + 1):
        create_user_obj(num=i)
    return


def create_staff_obj(num: int) -> None:
    category: Category = Category.objects.create(
        name=f'Категория {num}',
        slug=f'category-{num}',
    )
    subcategory: Subcategory = Subcategory.objects.create(
        name=f'Подкатегория {num}',
        slug=f'subcategory-{num}',
        category=category,
    )
    Good.objects.create(
        name=f'Товар {num}',
        slug=f'good-{num}',
        price=num,
        subcategory=subcategory,
    )
    return


@pytest.fixture()
def create_staff() -> None:
    """
    Фикстура для наполнения БД заданным числом
    товаров, категорий и подкотегорий.
    """
    for i in range(1, TEST_FIXTURES_OBJ_AMOUNT + 1):
        create_staff_obj(num=i)
    return


""""Эндпоинты API v1."""


URL_API_V1: str = '/api/v1/'

URL_AUTH: str = f'{URL_API_V1}auth/token/'
URL_AUTH_CREATE: str = f'{URL_AUTH}create/'
URL_AUTH_REFRESH: str = f'{URL_AUTH}refresh/'

URL_CATEGORIES: str = f'{URL_API_V1}categories/'

URL_CREATE_NUMS_ROW: str = f'{URL_API_V1}create-nums-row/'

URL_GOODS: str = f'{URL_API_V1}goods/'

URL_SHOPPING_CART: str = f'{URL_API_V1}shopping-cart/'
URL_SHOPPING_CART_CLEAR: str = f'{URL_SHOPPING_CART}clear_shopping_cart/'

URL_SUBCATEGORIES: str = f'{URL_API_V1}subcategories/'

URL_SWAGGER: str = f'{URL_API_V1}docs/swagger/'
