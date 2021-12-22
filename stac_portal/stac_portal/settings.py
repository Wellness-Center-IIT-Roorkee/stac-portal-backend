"""
Django settings for stac_portal project.
"""

from pathlib import Path
import yaml

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Parent directory for the project
PARENT_DIR = BASE_DIR.parent

# configuration file contains configurations for the app
CONFIGURATION_FILE = open(PARENT_DIR/'configurations/base.yml')

CONFIGURATION = yaml.safe_load(CONFIGURATION_FILE)

SECRETS = CONFIGURATION['secrets']
DATABASE = CONFIGURATION['services']['database']
EMAIL = CONFIGURATION['emails']
ENVIRONMENT = CONFIGURATION['environment']

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['secretKey']

OAUTH_CONFIGURATION = SECRETS['oAuth']
OAUTH_CLIENT_ID = OAUTH_CONFIGURATION['clientId']
OAUTH_CLIENT_SECRET = OAUTH_CONFIGURATION['clientSecret']
OAUTH_REDIRECT_URI = OAUTH_CONFIGURATION['redirectURI']

IS_PRODUCTION_ENV = not ENVIRONMENT['debug']
HOST_URL = ENVIRONMENT['hostURL']


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not IS_PRODUCTION_ENV

ALLOWED_HOSTS = [HOST_URL, ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'base_auth.apps.BaseAuthConfig',
    'stac_application.apps.StacApplicationConfig',
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

ROOT_URLCONF = 'stac_portal.urls'

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

WSGI_APPLICATION = 'stac_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DATABASE['name'],
        'USER': DATABASE['user'],
        'PASSWORD': DATABASE['password'],
        'HOST': DATABASE['host'],
        'PORT': DATABASE['port']
    }
}

AUTH_USER_MODEL = 'base_auth.User'

# TODO: Use cached sessions
SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'

SESSION_COOKIE_NAME = 'stac_session'

CSRF_COOKIE_NAME = 'stac_csrftoken'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static_files/'
STATIC_ROOT = PARENT_DIR/'static_files'

# Media files

MEDIA_URL = '/media/'
MEDIA_ROOT = PARENT_DIR/'media_files'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
