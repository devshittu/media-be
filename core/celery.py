import os
from celery import Celery
from django.conf import settings
from decouple import config


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# app = Celery('media-be')
app = Celery(config("APP_CODE_NAME", default="appname-media-be", cast=str))


app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# core/celery.py
