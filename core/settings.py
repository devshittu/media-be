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


# Identify the environment
ENVIRONMENT = config("APP_MEDIA_ENVIRONMENT", default="development")

# Example for toggling settings based on the environment
if ENVIRONMENT == "production":
    DEBUG = False
    # Other production-specific settings
else:
    DEBUG = True
    # Other development or test-specific settings

# DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    "web-app",
    "web-app-service",
    "127.0.0.1",
    "localhost",
    "*.mediaapp.local",
    "api.mediaapp.local",
    "app.mediaapp.local",
    "*.gong.ng",
    "api.gong.ng",
    "app.gong.ng",
    "api.staging.gong.ng",
    "app.staging.gong.ng",
    "api.dev.gong.ng",
    "app.dev.gong.ng",
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

    "https://api.gong.ng",
    "https://app.gong.ng",
    "https://api.staging.gong.ng",
    "https://app.staging.gong.ng",
    "https://api.dev.gong.ng",
    "https://app.dev.gong.ng",
    
    "http://frontend-app-service:3000",
    "https://frontend-app-service:3000",
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
    "support",
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
    
    'storages',
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
    "utils.middleware.LoggingMiddleware",
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
        "NAME": config(
            "POSTGRES_DB", default="mediabedb", cast=str
        ),  # Default value is 'mediabedb'
        "USER": config(
            "POSTGRES_USER", default="mediabeuser", cast=str
        ),  # Default value is 'mediabeuser'
        "PASSWORD": config(
            "POSTGRES_PASSWORD", default="mediabepassword", cast=str
        ),  # Default value is 'mediabepassword'
        "HOST": config(
            "POSTGRES_HOST", default="db-postgres", cast=str
        ),  # This should match the service name for Postgres in your docker-compose file
        "PORT": config(
            "POSTGRES_PORT", default="5432", cast=str
        ),  # Default port for PostgreSQL
    }
}


# Neo4J Database Configuration

NEO4J_USERNAME = config("NEO4J_USERNAME", default="neo4j")
NEO4J_PASSWORD = config("NEO4J_PASSWORD", default="password")
NEO4J_HOST = config(
    "NEO4J_HOST", default="db-neo4j"
)  # default could also be 'localhost'
NEO4J_PORT = config("NEO4J_PORT", default="7687")

NEOMODEL_NEO4J_BOLT_URL = (
    f"bolt://{NEO4J_USERNAME}:{NEO4J_PASSWORD}@{NEO4J_HOST}:{NEO4J_PORT}"
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


# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

if ENVIRONMENT == "development":
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


# Static & Media Files
# https://docs.djangoproject.com/en/4.2/howto/static-files/
# TODO: this works without the minio
STATIC_URL = "/staticfiles/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
# STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


MEDIA_URL = "/mediafiles/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
# TODO: this works without the minio


# # Assuming MinIO runs locally on port 9000 and you've set up a bucket named 'static'
# AWS_ACCESS_KEY_ID = "user"  # Use your MinIO access key
# AWS_SECRET_ACCESS_KEY = "password"  # Use your MinIO secret key
# AWS_STORAGE_BUCKET_NAME = "mybucket"
# # AWS_S3_ENDPOINT_URL = "http://minio:9000"# URL to your MinIO instance
# # AWS_S3_CUSTOM_DOMAIN = f"minio:9000"  # Use the internal Docker network name


# AWS_S3_ENDPOINT_URL = (
#     "https://minio.mediaapp.local"  # NGINX proxies to MinIO over HTTPS
# )
# AWS_S3_CUSTOM_DOMAIN = f"minio.mediaapp.local"

# AWS_S3_OBJECT_PARAMETERS = {
#     "CacheControl": "max-age=86400",
# }
# AWS_S3_USE_SSL = True
# AWS_LOCATION = "static"

# # Static files settings
# STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{AWS_LOCATION}/"
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"


# Authentication & Authorization
AUTH_USER_MODEL = "authentication.CustomUser"


# # Email configurations
# Environment-specific settings
if ENVIRONMENT == "development":
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = config(
        "APP_MEDIA_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
    )

EMAIL_HOST = config("APP_MEDIA_EMAIL_HOST", default="smtp.gmail.com")
EMAIL_USE_TLS = config("APP_MEDIA_EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_PORT = config("APP_MEDIA_EMAIL_PORT", default=587, cast=int)
EMAIL_HOST_USER = config("APP_MEDIA_EMAIL_HOST_USER", default="mshittu.work@gmail.com")
EMAIL_HOST_PASSWORD = config(
    "APP_MEDIA_EMAIL_HOST_PASSWORD", default="your_email_password"
)

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
    # TODO: for experimental purposes
    # "ACCESS_TOKEN_LIFETIME": timedelta(seconds=20),
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
        "utils.custom_jwt_authentication.CustomJWTAuthentication",
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
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
# AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
# AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")

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

SEEDING = False

if DEBUG:
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
            "media_be": {
                "handlers": ["console"],
                "level": "INFO",
                "propagate": True,
            },
            "global": {
                "handlers": ["console"],
                "level": "DEBUG",
                "propagate": True,
            },
        },
    }

# core/settings.py
