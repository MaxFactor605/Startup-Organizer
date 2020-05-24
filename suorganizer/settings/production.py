import os
import dj_database_url
from .base import *

DEBUG = False
TEMPLATE_DEBUG = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': dj_database_url.config()
}

'8$2(j1asy+2t113v%7%#qdntydt_@voxs3rz#7)&2u+66i!y0f'
