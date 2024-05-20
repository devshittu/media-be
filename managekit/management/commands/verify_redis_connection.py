from django.core.management.base import BaseCommand
from celery import Celery
from django.conf import settings


class Command(BaseCommand):
    help = "Verify connection to Redis"

    def handle(self, *args, **kwargs):
        broker_url = settings.CELERY_BROKER_URL
        app = Celery("tasks", broker=broker_url)
        try:
            app.connection().connect()
            self.stdout.write(self.style.SUCCESS("Connection to Redis successful!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Connection to Redis failed: {e}"))

# python manage.py verify_redis_connection
# managekit/management/commands/verify_redis_connection.py
