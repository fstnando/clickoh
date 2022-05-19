"""
Django settings for clickoh project.

Generated by 'django-admin startproject' using Django 3.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
#SECRET_KEY = 'django-insecure-5una&750%7i()+^fjf4ul%wka=mjj=&!jsk81%c^t!@zb8iar0'
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (os.environ['DJ_DEBUG'] == 'True')
#DEBUG = True

# Application definition

INSTALLED_APPS = [
    # librerias basicas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # librerias externas utilizadas
    'rest_framework_simplejwt',
    'drf_yasg',
    'rest_framework',
    'django_filters',
    'corsheaders',

    # Incorporamos las librerias/Apps propias
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'clickoh.urls'

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

WSGI_APPLICATION = 'clickoh.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'es'

TIME_ZONE = 'America/Argentina/Buenos_Aires'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # Se define las formas de autenticación
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # Se define la autenticación por token Simple JWT
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}


CORS_ALLOW_ALL_ORIGINS = True

if DEBUG:
    ALLOWED_HOSTS = []
else:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.herokuapp.com']
    #ALLOWED_HOSTS = ['*']

    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_TMP = os.path.join(BASE_DIR, 'static')
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

    os.makedirs(STATIC_ROOT, exist_ok=True)
    os.makedirs(STATIC_TMP, exist_ok=True)

    #DATABASES['default'] = dj_database_url.config(conn_max_age=600)
    DATABASES['default'] = dj_database_url.config(default=config('DATABASE_URL'), conn_max_age=600, ssl_require=True)
    CSRF_TRUSTED_ORIGINS = ["https://clickoh.herokuapp.com"]

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': ('%(asctime)s [%(process)d] [%(levelname)s] '
                           'pathname=%(pathname)s lineno=%(lineno)s '
                           'funcname=%(funcName)s %(message)s'),
                'datefmt': '%Y-%m-%d %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'null': {
                'level': 'DEBUG',
                'class': 'logging.NullHandler',
            },
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': False,
            },
        }
    }
