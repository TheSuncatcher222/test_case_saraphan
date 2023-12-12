import os

from backend.settings import (
    BASE_DIR, DEBUG,
    DATABASES, DB_ENGINE, DB_HOST, DB_NAME, DB_PASSWORD,
    DATABASE_POSTGRESQL, DB_PORT, DB_USER,
    SECRET_KEY,
)


class TestProdSettings():
    """Производит тест настроек проекта перед деплоем на сервер."""

    def test_db_is_postgresql(self) -> None:
        """Проверяет, что база данных проекта: PostgreSQL."""
        assert DATABASES == DATABASE_POSTGRESQL, (
            'Установите для settings.DATABASES '
            'значение app.data.DB_POSTGRESQL.'
        )
        return

    def test_debug_is_false(self) -> None:
        """Проверяет, что DEBUG=False."""
        assert not DEBUG, 'Установите для settings.DEBUG значение False.'
        return

    def test_env(self) -> None:
        """
        Проверяет, что в проекте существует .env файл,
        который содержит все необходимые поля.
        """
        env_file_path = os.path.join(BASE_DIR, '.env')
        assert os.path.isfile(env_file_path), 'Создайте .env файл.'
        missed_fields: list[str] = []
        ENV_DATA: dict[str, any] = {
            'DB_ENGINE': DB_ENGINE,
            'DB_HOST': DB_HOST,
            'DB_NAME': DB_NAME,
            'DB_PASSWORD': DB_PASSWORD,
            'DB_PORT': DB_PORT,
            'DB_USER': DB_USER,
            'SECRET_KEY': SECRET_KEY,
        }
        for key, value in ENV_DATA.items():
            if value is None:
                missed_fields.append(key)
        assert not missed_fields, (
            'В .env файле отсутствуют следующие поля: '
            f'{", ".join(field for field in missed_fields)}'
        )
        return
