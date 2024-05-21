from django.core.management.base import BaseCommand
from django.db import connections, OperationalError
from django.conf import settings
import os


class Command(BaseCommand):
    help = "Verify connection to PostgreSQL database"

    def handle(self, *args, **kwargs):
        db_conn = connections["default"]

        self.stdout.write(
            self.style.SUCCESS(f"POSTGRES_DB: {os.getenv('POSTGRES_DB', 'mediabedb')}")
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"POSTGRES_USER: {os.getenv('POSTGRES_USER', 'mediabeuser')}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"POSTGRES_PASSWORD: {os.getenv('POSTGRES_PASSWORD', 'mediabepassword')}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(
                f"POSTGRES_HOST: {os.getenv('POSTGRES_HOST', 'db-postgres')}"
            )
        )
        self.stdout.write(
            self.style.SUCCESS(f"POSTGRES_PORT: {os.getenv('POSTGRES_PORT', '5432')}")
        )

        try:
            db_conn.cursor()
            self.stdout.write(
                self.style.SUCCESS("Connection to PostgreSQL successful!")
            )
        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f"Connection to PostgreSQL failed: {e}"))


# Save this as managekit/management/commands/verify_postgres_connection.py
# Usage: python manage.py verify_postgres_connection
