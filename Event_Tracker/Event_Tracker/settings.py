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
import ssl
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')  # Needed when using Heroku's routing



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ue^+9e_v_tj^n#(dv_drkql+m$b*lp1&3(!0x6jar)*a)9#5!d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['event.sharetunez.me','127.0.0.1']


# Celery settings
# CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
# CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379')

CELERY_BROKER_URL = os.getenv('REDIS_TLS_URL')
CELERY_RESULT_BACKEND = os.getenv('REDIS_TLS_URL')


# Optional: configure Celery to use JSON
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Optional: set timezone
CELERY_TIMEZONE = 'UTC'

# Add SSL options
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'ssl_cert_reqs': ssl.CERT_NONE,
    # 'ssl_ca_certs': '/path/to/ca-certificates.crt',  # Optional
}

CELERY_RESULT_TRANSPORT_OPTIONS = {
    'ssl_cert_reqs': ssl.CERT_NONE,
    # 'ssl_ca_certs': '/path/to/ca-certificates.crt',  # Optional
}

# Application definition

INSTALLED_APPS = [
    'event',
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
    'django_celery_results',
    'frontend.apps.FrontendConfig'
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
    "whitenoise.middleware.WhiteNoiseMiddleware",
]
#Whitelist React host
CORS_ORIGIN_WHITELIST = [
    'http://localhost:3000',
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

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

STATIC_URL = '/staticfiles/'

STATICFILES_DIRS = [
    BASE_DIR / "event/static",
]

MEDIA_ROOT = os.path.join(BASE_DIR,'media') #Media Upload folder

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/' # can make this whatever url to generate files urls


# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#Auth Info
# Eventtracker\settings.py
SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
SOCIAL_AUTH_AUTH0_DOMAIN = 'dev-i24h8c02hqxkdod3.us.auth0.com'
SOCIAL_AUTH_AUTH0_KEY = 'Qn1a6hYltuPliZU0QedcxnTkNiGQj1bs'
SOCIAL_AUTH_AUTH0_SECRET = 'sSqwHp5PyoPaneApgPEcFwJt1yRynpifJ4qOEbv0-mBreL4Jhy_RqSY_mgFQQToa'

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