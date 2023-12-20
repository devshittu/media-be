# Standard Library Imports
from pathlib import Path
from datetime import timedelta
import os

# Third-party Imports
from decouple import config

# Application-specific Imports
from utils.constants import DEFAULT_PAGE_SIZE

# Constants
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Security
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
SECRET_KEY = config(
    "DJANGO_SECRET_KEY",
    default="django-insecure-f8fzco37jytbzpl&kv6f(^fn^r*o4luzlttw7k@zfat)7#-q_0",
    cast=str,
)
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = [
    "web-app",
    "127.0.0.1",
    "localhost",
    "*.mediaapp.local",
    "api.mediaapp.local",
    "app.mediaapp.local",
]

# Cross Origin Resource
CORS_ORIGIN_ALLOW_ALL = True

# CORS_ALLOWED_ORIGINS = [
# #     "http://media-fe:3000",  # Docker service name for the frontend
# #     "http://localhost:3000",  # For local development
# #     "http://127.0.0.1:3000",  # Also for local development
# #     "http://0.0.0.0:3000",  # Replace with your frontend domain
#     # "http://api.media-app-fe.com:3000",
#     "http://app.mediaapp.local",
#     "https://app.mediaapp.local",
#     "http://api.mediaapp.local",
#     "https://api.mediaapp.local",
# ]
CORS_ALLOW_HTTPS = True

CSRF_TRUSTED_ORIGINS = [
    "http://api.mediaapp.local",
    "https://api.mediaapp.local",
    "http://app.mediaapp.local",
    "https://app.mediaapp.local",
    "http://web-app:8000",
    "https://web-app:8000",
    "http://localhost:3000",
    "http://localhost:3001",
]

CORS_ALLOW_CREDENTIALS = True


# Application definition

CUSTOM_APPS = [
    "authentication",
    "users",
    "system_messaging",
    "multimedia",
    "stories",
    "support"
    # "analytics",
    # ... any other custom apps ...
]

INSTALLED_APPS = [
    # Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Thirdparty Apps
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "django_extensions",
    "ckeditor",
    # 'ckeditor_uploader',  # If you want image uploading
    "django_neomodel",
    "corsheaders",
    # Custom Apps
    "authentication",
    "users.apps.UsersConfig",
    "system_messaging",
    "multimedia",
    "analytics",
    "stories",
    "managekit",
    "feedback",
    "support",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# URLs & WSGI
ROOT_URLCONF = "core.urls"
WSGI_APPLICATION = "core.wsgi.application"

# Database Configuration
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get(
            "POSTGRES_DB", "mediabedb"
        ),  # Default value is 'mediabedb'
        "USER": os.environ.get(
            "POSTGRES_USER", "mediabeuser"
        ),  # Default value is 'mediabeuser'
        "PASSWORD": os.environ.get(
            "POSTGRES_PASSWORD", "mediabepassword"
        ),  # Default value is 'mediabepassword'
        "HOST": "db-postgres",  # This should match the service name for Postgres in your docker-compose file
        "PORT": "5432",  # Default port for PostgreSQL
    }
}

# Neo4j Configuration
NEOMODEL_NEO4J_BOLT_URL = "bolt://neo4j:password@db-neo4j:7687"
NEOMODEL_NEO4J_AUTH = (
    config("NEOMODEL_NEO4J_AUTH_USERNAME", default="neo4j", cast=str),
    config("NEOMODEL_NEO4J_AUTH_PASSWORD", default="password", cast=str),
)

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static & Media Files
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")
MEDIA_URL = "/media/"

# Authentication & Authorization
AUTH_USER_MODEL = "authentication.CustomUser"
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"  # For development
# Use email for authentication instead of usernames
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False

AUTHENTICATION_BACKENDS = [
    "authentication.authentication_backends.EmailOrUsernameModelBackend",
]

# Possible values: 'VERIFICATION_LINK', 'OTP'
ACCOUNT_VERIFICATION_METHOD = "OTP"  # or 'VERIFICATION_LINK'

# Email Configuration
# Require email confirmation before allowing login
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# For development, use the console backend to display sent emails
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
}


# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        # 'rest_framework_simplejwt.authentication.JWTStatelessUserAuthentication',
    ),
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.CustomPageNumberPagination",
    "PAGE_SIZE": DEFAULT_PAGE_SIZE,  # Adjust this number based on how many records you want per page
    "DEFAULT_FILTER_BACKENDS": ["rest_framework.filters.OrderingFilter"],
    "EXCEPTION_HANDLER": "utils.handlers.custom_exception_handler",
}
# constants for rest framework
POSTS_PER_PAGE = config("POSTS_PER_PAGE", default=10, cast=int)
ANCESTORS_PER_PAGE = config("ANCESTORS_PER_PAGE", default=4, cast=int)
DESCENDANTS_PER_PAGE = config("DESCENDANTS_PER_PAGE", default=5, cast=int)


# AWS, Google Cloud & Twilio Configuration
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")

GS_BUCKET_NAME = config("GS_BUCKET_NAME")
GS_CREDENTIALS = config("GS_CREDENTIALS")
GS_PROJECT_ID = config("GS_PROJECT_ID")

TWILIO_ACCOUNT_SID = config("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = config("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = config("TWILIO_PHONE_NUMBER")


# CKEditor Configuration
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": 800,
    },
}
CKEDITOR_UPLOAD_PATH = "uploads/"


# Test runner
TEST_RUNNER = "pytest_django.runner.DjangoTestSuiteRunner"


# Celery configurations
CELERY_BROKER_URL = config(
    "CELERY_BROKER_URL", default="redis://redis:6379/0", cast=str
)
CELERY_RESULT_BACKEND = config(
    "CELERY_RESULT_BACKEND", default="redis://redis:6379/0", cast=str
)
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
# core/settings.py


SEEDING = False


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "media_be": {  # Replace 'your_app_name' with the name of your Django app
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
