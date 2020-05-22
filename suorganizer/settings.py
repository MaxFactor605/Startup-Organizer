"""
Django settings for suorganizer project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
import os
from pathlib import Path
from .log_filters import ManagmentFilter
from django.urls import reverse_lazy

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm15(!engh08!wl#z#06s^#e+&2#n^_#ozm21)wrynjrzbo&f9e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '192.168.0.109',
    '127.0.0.1',
                 ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'suorganizer',
    'organizer',
    'blog',
    'user',
    'contact',
    'core',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
verbose = (
    "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(messages)s"
)
"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
      'remove_migration_sql': {
          '()': ManagmentFilter
      }
    },
    'handlers': {
        'console': {
            'filters': ['remove_migration_sql'],
            'class': 'logging.StreamHandler',
        },
    },
    'formatters': {
        'verbose':{
            'format': verbose,
            'datefmt': '%Y-%b-%d %H:%M:%S',
        },
    },
    'loggers': {
        'django': {
            'handlers' : ['console'],
            'level': 'DEBUG',
            'formatter': 'verbose',
        },

    },
}
"""
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'suorganizer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators

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
# Login Settings
LOGIN_URL = reverse_lazy('user_login')
LOGIN_REDIRECT_URL = reverse_lazy('blog_post_list')
LOGOUT_URL = reverse_lazy('user_logout')

# Email Settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'alexandow.maxim1@gmail.com'
EMAIL_HOST_PASSWORD = 'All5671234'
SERVER_EMAIL = 'contact@test.com'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'alexandow.maxim1@gmail.com'
EMAIL_SUBJECT_PREFIX = '[Startup Organizer]'
MANAGERS = (
    ('Us', 'ourselves@test.com'),
)
# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

ROOT_URLCONF = 'suorganizer.urls'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]