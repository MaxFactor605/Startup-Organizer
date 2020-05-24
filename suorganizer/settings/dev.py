from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    '192.168.0.109',
    '127.0.0.1',
                 ]

INTERNAL_IPS =[
    '127.0.0.1',
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SECRET_KEY = 'm15(!engh08!wl#z#06s^#e+&2#n^_#ozm21)wrynjrzbo&f9e'

