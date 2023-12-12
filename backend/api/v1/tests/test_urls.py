import pytest

from api.v1.tests.fixtures import (
    URL_MISSED_STATUSES,
    URL_AUTH_CREATE, URL_AUTH_REFRESH, URL_CATEGORIES, URL_CREATE_NUMS_ROW,
    URL_SHOPPING_CART, URL_SUBCATEGORIES, URL_SWAGGER,
    client_auth,
)


@pytest.mark.django_db
class TestEndpointsAvailability():
    """
    Производит тест доступности эндпоинтов в urlpatterns.
    """

    @pytest.mark.parametrize(
        'url, meaning', [
            (URL_AUTH_CREATE,
             'получения пары токенов доступа и обновления'
             ),
            (URL_AUTH_REFRESH,
             'обновления токена доступа'
             ),
            (URL_CATEGORIES,
             'получения списка категорий товаров'
             ),
            (URL_CREATE_NUMS_ROW,
             'формирования списка цифр'
             ),
            (URL_SHOPPING_CART,
             'взаимодействия с корзиной товаров'
             ),
            (URL_SUBCATEGORIES,
             'получения списка подкатегорий товаров'
             ),
            (URL_SWAGGER,
             'получения swagger-представления документации API'
             ),
        ]
    )
    def test_ping(self, url, meaning) -> None:
        """Производит тест доступности эндпоинтов JWT."""
        response = client_auth().get(url)
        assert response.status_code not in URL_MISSED_STATUSES, (
            f'Убедитесь, что эндпоинт {meaning} функционирует '
            f'и доступен по адресу "{url}".'
        )
        return
