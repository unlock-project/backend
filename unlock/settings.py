"""
Django settings for unlock project.

Generated by 'django-admin startproject' using Django 4.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(".env")

EMAIL_HOST = os.getenv('UNLOCK_EMAIL_HOST')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('UNLOCK_SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('UNLOCK_DEBUG', 'false').lower().strip(' "\'') == 'true'

ALLOWED_HOSTS = os.getenv('UNLOCK_ALLOWED_HOSTS', '').split(' ')

CSRF_TRUSTED_ORIGINS = os.getenv('UNLOCK_CSRF_TRUSTED_ORIGINS', '').split(' ')


# ADD UNLOCK_CSRF_TRUSTED_ORIGINS, UNLOCK_BOT_URL TO ENV VARS

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'polymorphic',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users_app',
    'bot_app',
    'events_app',
    'score_app',
    'admin_app',
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

ROOT_URLCONF = 'unlock.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'unlock.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_ENGINE = 'django.db.backends.sqlite3'
DATABASE_NAME = BASE_DIR / os.getenv('UNLOCK_DATABASE_NAME', 'db.sqlite3')

if os.getenv('UNLOCK_DATABASE') == 'postgres':
    DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2'
    DATABASE_NAME = os.getenv('UNLOCK_DATABASE_NAME')

DATABASES = {
    'default': {
        'ENGINE': DATABASE_ENGINE,
        'HOST': os.getenv('UNLOCK_DATABASE_HOST'),
        'PORT': os.getenv('UNLOCK_DATABASE_PORT'),
        'NAME': DATABASE_NAME,
        'USER': os.getenv('UNLOCK_DATABASE_USER'),
        'PASSWORD': os.getenv('UNLOCK_DATABASE_PASSWORD')
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# if DEBUG:
#     STATICFILES_DIRS = [
#        BASE_DIR / 'static'
#     ]
# else:
STATIC_ROOT = 'static'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
AUTH_USER_MODEL = 'users_app.User'

BOT_URL = os.getenv('UNLOCK_BOT_URL', '')

LOGIN_REDIRECT_URL = '/'