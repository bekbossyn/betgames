# -*- coding: utf-8 -*-
"""
Django settings for betgames project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pjy7lr#dod33u&&5g#6@8861$ymtb5@q#0@3&da-x$kn882c7g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'django_celery_beat',
    'game'
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

ROOT_URLCONF = 'betgames.urls'

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

WSGI_APPLICATION = 'betgames.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
AUTH_USER_MODEL = "main.MyUser"
AUTHENTICATION_BACKENDS = ('main.backends.email_backend.CaseInsensitiveModelBackend', )

JWT_KEY = 'betmates-secret-key4512'
JWT_ALGORITHM = 'HS256'

AUTH_TOKEN_HEADER_NAME = ["AUTH_TOKEN", "HTTP_AUTH_TOKEN", "Auth-Token"]
AUTH_TOKEN_COOKIE_NAME = "auth-token"

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

SMS_MOBIZON_KEY = "abc8c3089cd18f2b345d12ff251f7ed4e97a737c"
SMS_SEND_URL = "https://api.mobizon.com/service/message/sendsmsmessage"
GET_SMS_STATUS = "https://api.mobizon.com/service/message/getsmsstatus"
USER_INFO = "https://api.mobizon.com/service/user/getownbalance"
SHORTIFY_LINK = "https://api.mobizon.com/service/link/create"


ADMINS_LIST = ['dakzholov@gmail.com', 'j.rauan@gmail.com', 'betmates7@gmail.com']

ADMINS = (
    ('Darkhan', 'dakzholov@gmail.com'),
    ('Rocki', 'j.rauan@gmail.com'),
    ('Beks', 'betmates7@gmail.com'),
)


# Mail settings
FROM_EMAIL = u'BettyMates API <betmates7@gmail.com>'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'betmates7@gmail.com'
EMAIL_HOST_PASSWORD = 'truesight7'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

