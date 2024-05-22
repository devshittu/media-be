from django.core.management.base import BaseCommand
from django.conf import settings
from neomodel import config, db
from celery import Celery
from django.db import connections, OperationalError
import os


class Command(BaseCommand):
    help = "Verify connections to various services"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--services",
            nargs="+",
            type=str,
            help="The services to check: neo4j, redis, postgres or all",
        )

    def handle(self, *args, **kwargs):
        services = kwargs["services"]

        if "all" in services:
            services = ["neo4j", "redis", "postgres"]

        for service in services:
            self.stdout.write(
                self.style.SUCCESS(f"Checking connection for {service}...")
            )
            if service == "neo4j":
                self.verify_neo4j_connection()
            elif service == "redis":
                self.verify_redis_connection()
            elif service == "postgres":
                self.verify_postgres_connection()
            else:
                self.stdout.write(self.style.ERROR(f"Unknown service: {service}"))

    def verify_neo4j_connection(self):
        self.stdout.write(
            self.style.SUCCESS(f"NEO4J_USERNAME: {os.getenv('NEO4J_USERNAME')}")
        )
        self.stdout.write(
            self.style.SUCCESS(f"NEO4J_PASSWORD: {os.getenv('NEO4J_PASSWORD')}")
        )
        self.stdout.write(self.style.SUCCESS(f"NEO4J_HOST: {os.getenv('NEO4J_HOST')}"))
        self.stdout.write(self.style.SUCCESS(f"NEO4J_PORT: {os.getenv('NEO4J_PORT')}"))
        self.stdout.write(
            self.style.SUCCESS(
                f"NEOMODEL_NEO4J_BOLT_URL: {settings.NEOMODEL_NEO4J_BOLT_URL}"
            )
        )

        config.DATABASE_URL = settings.NEOMODEL_NEO4J_BOLT_URL

        try:
            db.cypher_query("MATCH (n) RETURN n LIMIT 1")
            self.stdout.write(self.style.SUCCESS("Connection to Neo4j successful!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Connection to Neo4j failed: {e}"))

    def verify_redis_connection(self):
        broker_url = settings.CELERY_BROKER_URL
        app = Celery("tasks", broker=broker_url)

        try:
            app.connection().connect()
            self.stdout.write(self.style.SUCCESS("Connection to Redis successful!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Connection to Redis failed: {e}"))

    def verify_postgres_connection(self):
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

# python manage.py verify_connection -s all
# python manage.py verify_connection --services all
# python manage.py verify_connection -s neo4j redis postgres
# python manage.py verify_connection --services neo4j redis postgres

# python manage.py verify_connection
# managekit/management/commands/verify_connection.py
