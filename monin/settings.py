# coding: utf-8
"""
Django settings for monin project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from django.utils.translation import ugettext_lazy as _

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3yjg0c3v8w42dznwt3=fwg%=)x=2)f!3$!h)ycfqpeoh=x_9^_'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'south',
    'registration',
    'storages',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "django.core.context_processors.csrf",
    "main.custom_context.config",
)

ROOT_URLCONF = 'monin.urls'

WSGI_APPLICATION = 'monin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Database settings to heroku deploy
import dj_database_url
DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'es'
LOCALE_PATHS = (
    'locale',
)

LANGUAGES = (
  ('es', _('Espanol')),
  ('en', _('Ingles')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

COLORS = (
  ('negro', _('Negro')),
  ('blanco', _('Blanco')),
  ('beige', _('Biege')),
  ('marino', _('Marino')),
)

SIZES = (
  ('1', 1),
  ('2', 2),
  ('3', 3),
  ('4', 4),
  ('5', 5),
  ('6', 6),
  ('7', 7),
  ('8', 8),
  ('9', 9),
  ('10', 10),
  ('11', 11),
  ('12', 12),
  ('13', 13),
  ('14', 14),
  ('15', 15),
  ('16', 16),
)

MEDIA_URL = '/'

MEDIA_ROOT = ''

STATIC_ROOT = ''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

# Parse database configuration from $DATABASE_URL
import dj_database_url
DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, 'static'),
#)

FROM = 'info@monin.com.mx'
TO = 'omr_123@hotmail.com' #'guillermoalvarado89@gmail.com'
SUBJECT = '[Monin] Aviso de la página'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# AWS Settings
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = S3_URL
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
AWS_HEADERS = {
  'Cache-Control': 'max-age=86400',
}
AWS_QUERYSTRING_EXPIRE = 631152000
AWS_QUERYSTRING_AUTH = False
AWS_PRELOAD_METADATA = True

if os.environ.get('DEVELOPMENT_ENVIRONMENT') and os.environ.get('DEVELOPMENT_ENVIRONMENT') == 'True':
    from local_settings import *

