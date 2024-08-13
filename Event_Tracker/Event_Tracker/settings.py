"""
Django settings for Event_Tracker project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path




# Build paths inside the project like this: BASE_DIR / 'subdir'.
import os
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ue^+9e_v_tj^n#(dv_drkql+m$b*lp1&3(!0x6jar)*a)9#5!d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['event.sharetunez.me','127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'event',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social_django',
    'corsheaders',
    'rest_framework',
    'phonenumber_field',
    'qr_code',
    'frontend.apps.FrontendConfig'
]

# Use channels layer as the default backend for `asgi`
ASGI_APPLICATION = 'Event_Tracker.routing.application'

# Channels settings
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
#Whitelist React host
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
]

ROOT_URLCONF = 'Event_Tracker.urls'

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

WSGI_APPLICATION = 'Event_Tracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
    "/var/www/static/",
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = os.path.join(BASE_DIR,'media') #Media Upload folder

MEDIA_URL = '/media/' # can make this whatever url to generate files urls


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Auth Info
# Eventtracker\settings.py
SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
SOCIAL_AUTH_AUTH0_DOMAIN = 'dev-nrvj4wk4.us.auth0.com'
SOCIAL_AUTH_AUTH0_KEY = 'nv0qZulilI6O7c5K3LAzOF6pZg7JeI7c'
SOCIAL_AUTH_AUTH0_SECRET = 'D1mmMnVt-PTLiCJ98LYM5KRcnqo89vQaTfBtNnBUqkEJSgdnjeJQdYxWyGnuNKje'

#Scope used by Auth0
# Eventtracker\settings.py
SOCIAL_AUTH_AUTH0_SCOPE = [
    'openid',
    'profile',
    'email'
]

#Used for Django to authenticate in the backend and users to login 
# Eventtracker\settings.py
AUTHENTICATION_BACKENDS = {
    'event.auth0backend.Auth0',
    'django.contrib.auth.backends.ModelBackend'
}

#Configure the login, redirect login and redirect logout URLs 
# Eventtracker\settings.py
LOGIN_URL = '/login/auth0'
LOGIN_REDIRECT_URL = '/host/event/home/'