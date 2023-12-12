from backend.settings import *  # noqa (F401)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # noqa (F405)
        'ATOMIC_REQUESTS': True,
    }
}
