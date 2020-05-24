import os
import dj_database_url
from .base import *

DEBUG = False
TEMPLATE_DEBUG = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

DATABASES = {
    'default': dj_database_url.config()
}

