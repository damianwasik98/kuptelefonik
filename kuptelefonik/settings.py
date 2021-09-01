"""
Django settings for kuptelefonik project.

Generated by 'django-admin startproject' using Django 3.0.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import dj_database_url
from dotenv import load_dotenv

from django.core.management.utils import get_random_secret_key

load_dotenv() #load .env file with secure variables


class InvalidEnv(Exception):

    def __init__(self, env_key, env_val):
        self.env_key = env_key
        self.env_val = env_val
    
    def __str__(self):
        return f"\"{self.env_val}\" is invalid value for env \"{self.env_key}\""


def load_debug_env():
    env_key = "DEBUG"
    env = os.getenv(env_key, False)
    if env is False:
        return env

    env_cast_map = {
        "true": True,
        "false": False
    }

    try:
        return env_cast_map[env.lower()]
    except KeyError:
        raise InvalidEnv(env_key=env_key, env_val=env)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = load_debug_env()

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.dashboard',
    'rest_framework'
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

ROOT_URLCONF = 'kuptelefonik.urls'

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

WSGI_APPLICATION = 'kuptelefonik.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

def load_db_url():
    """
    url schema https://github.com/jacobian/dj-database-url#url-schema
    """
    env_key = "DATABASE_URL"
    default_sqlite_path = os.path.join(BASE_DIR, "db.sqlite3")
    env = os.getenv(env_key, f"sqlite:///{default_sqlite_path}")
    try:
        return dj_database_url.parse(env)
    except KeyError:
        raise InvalidEnv(env_key=env_key, env_val=env)


DATABASES = {
    "default": load_db_url()
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Auth
LOGIN_REDIRECT_URL = "/dashboard"
LOGOUT_REDIRECT_URL = "/accounts/login"