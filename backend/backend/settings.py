from datetime import timedelta
import os
from pathlib import Path

from corsheaders.defaults import default_headers
from dotenv import load_dotenv

load_dotenv()


"""App settings."""


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

DEBUG = os.getenv('DEBUG')
if DEBUG == 'True':
    DEBUG = True
else:
    DEBUG = False

DEBUG_DATABASE = os.getenv('DEBUG_DATABASE')
if DEBUG_DATABASE == 'True':
    DEBUG_DATABASE = True
else:
    DEBUG_DATABASE = False


"""Django settings."""


DB_ENGINE = os.getenv('DB_ENGINE')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('POSTGRES_DB')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')

DATABASE_POSTGRESQL = {
    'default': {
        'ENGINE': DB_ENGINE,
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

DATABASE_SQLITE = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES = DATABASE_SQLITE if DEBUG_DATABASE else DATABASE_POSTGRESQL

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party
    'drf_spectacular',
    'rest_framework',
    # Local
    'api',
    'goods',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Saraphan API",
    "VERSION": "0.0.1",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SCHEMA_PATH_PREFIX": r'/api/v1/',
}

ROOT_URLCONF = 'backend.urls'

WSGI_APPLICATION = 'backend.wsgi.application'


"""Models settings."""


ADMIN_ITEMS_PER_PAGE = 15

CATEGORY_IMAGE_PATH: str = 'categories/'
CATEGORY_NAME_MAX_LEN: int = 30
CATEGORY_SLUG_MAX_LEN: int = 30

GOOD_IMAGE_PATH: str = 'goods/'

SHOPPING_CART_MIN_AMOUNT: int = 1

SUBCATEGORY_IMAGE_PATH: str = 'subcategories/'
SUBCATEGORY_NAME_MAX_LEN: int = 30
SUBCATEGORY_SLUG_MAX_LEN: int = 30


def set_category_image_name(instance, filename) -> str:
    """Формирует название имени файла изображения для Category."""
    return f'{CATEGORY_IMAGE_PATH}{instance.slug}'


def set_good_image_l_name(instance, filename) -> str:
    """Формирует название имени файла изображения (L) для Good."""
    return f'{GOOD_IMAGE_PATH}{instance.slug}_l'


def set_good_image_m_name(instance, filename) -> str:
    """Формирует название имени файла изображения (M) для Good."""
    return f'{GOOD_IMAGE_PATH}{instance.slug}_m'


def set_good_image_s_name(instance, filename) -> str:
    """Формирует название имени файла изображения (S) для Good."""
    return f'{GOOD_IMAGE_PATH}{instance.slug}_s'


def set_subcategory_image_name(instance, filename) -> str:
    """Формирует название имени файла изображения для Subcategory."""
    return f'{SUBCATEGORY_IMAGE_PATH}{instance.slug}'


"""Static files settings."""


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATIC_URL = 'static/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


"""Regional settings."""


LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


"""Security settings."""


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    *default_headers,
    "access-control-allow-credentials",
]

CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = [
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

SECRET_KEY = os.getenv('SECRET_KEY')
