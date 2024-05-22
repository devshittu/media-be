# from django.core.management.base import BaseCommand
# from django.conf import settings
# from neomodel import config, db
# from celery import Celery
# from django.db import connections, OperationalError
# import os


# class Command(BaseCommand):
#     help = "Verify connections to various services"

#     def add_arguments(self, parser):
#         parser.add_argument(
#             "-s",
#             "--services",
#             nargs="+",
#             type=str,
#             help="The services to check: neo4j, redis, postgres or all",
#         )

#     def handle(self, *args, **kwargs):
#         services = kwargs["services"]

#         if "all" in services:
#             services = ["neo4j", "redis", "postgres"]

#         for service in services:
#             self.stdout.write(
#                 self.style.SUCCESS(f"Checking connection for {service}...")
#             )
#             if service == "neo4j":
#                 self.verify_neo4j_connection()
#             elif service == "redis":
#                 self.verify_redis_connection()
#             elif service == "postgres":
#                 self.verify_postgres_connection()
#             else:
#                 self.stdout.write(self.style.ERROR(f"Unknown service: {service}"))

#     def verify_neo4j_connection(self):
#         self.stdout.write(
#             self.style.SUCCESS(f"NEO4J_USERNAME: {os.getenv('NEO4J_USERNAME')}")
#         )
#         self.stdout.write(
#             self.style.SUCCESS(f"NEO4J_PASSWORD: {os.getenv('NEO4J_PASSWORD')}")
#         )
#         self.stdout.write(self.style.SUCCESS(f"NEO4J_HOST: {os.getenv('NEO4J_HOST')}"))
#         self.stdout.write(self.style.SUCCESS(f"NEO4J_PORT: {os.getenv('NEO4J_PORT')}"))
#         self.stdout.write(
#             self.style.SUCCESS(
#                 f"NEOMODEL_NEO4J_BOLT_URL: {settings.NEOMODEL_NEO4J_BOLT_URL}"
#             )
#         )

#         config.DATABASE_URL = settings.NEOMODEL_NEO4J_BOLT_URL

#         try:
#             db.cypher_query("MATCH (n) RETURN n LIMIT 1")
#             self.stdout.write(self.style.SUCCESS("Connection to Neo4j successful!"))
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"Connection to Neo4j failed: {e}"))

#     def verify_redis_connection(self):
#         broker_url = settings.CELERY_BROKER_URL
#         app = Celery("tasks", broker=broker_url)

#         try:
#             app.connection().connect()
#             self.stdout.write(self.style.SUCCESS("Connection to Redis successful!"))
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(f"Connection to Redis failed: {e}"))

#     def verify_postgres_connection(self):
#         db_conn = connections["default"]

#         self.stdout.write(
#             self.style.SUCCESS(f"POSTGRES_DB: {os.getenv('POSTGRES_DB', 'mediabedb')}")
#         )
#         self.stdout.write(
#             self.style.SUCCESS(
#                 f"POSTGRES_USER: {os.getenv('POSTGRES_USER', 'mediabeuser')}"
#             )
#         )
#         self.stdout.write(
#             self.style.SUCCESS(
#                 f"POSTGRES_PASSWORD: {os.getenv('POSTGRES_PASSWORD', 'mediabepassword')}"
#             )
#         )
#         self.stdout.write(
#             self.style.SUCCESS(
#                 f"POSTGRES_HOST: {os.getenv('POSTGRES_HOST', 'db-postgres')}"
#             )
#         )
#         self.stdout.write(
#             self.style.SUCCESS(f"POSTGRES_PORT: {os.getenv('POSTGRES_PORT', '5432')}")
#         )

#         try:
#             db_conn.cursor()
#             self.stdout.write(
#                 self.style.SUCCESS("Connection to PostgreSQL successful!")
#             )
#         except OperationalError as e:
#             self.stdout.write(self.style.ERROR(f"Connection to PostgreSQL failed: {e}"))

# # python manage.py verify_connection -s all
# # python manage.py verify_connection --services all
# # python manage.py verify_connection -s neo4j redis postgres
# # python manage.py verify_connection --services neo4j redis postgres

# # python manage.py verify_connection
# # managekit/management/commands/verify_connection.py


from django.core.management.base import BaseCommand
from django.conf import settings
from neomodel import config, db
from celery import Celery
from django.db import connections, OperationalError
from decouple import config as env_config
import os


class Command(BaseCommand):
    help = "Verify connections to various services"

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--services",
            nargs="+",
            type=str,
            default=["all"],
            help="The services to check: neo4j, redis, postgres or all",
        )
        parser.add_argument(
            "-d",
            "--debug",
            action="store_true",
            help="Enable detailed debug output",
        )

    def handle(self, *args, **kwargs):
        services = kwargs["services"]
        debug = kwargs["debug"]

        if "all" in services:
            services = ["neo4j", "redis", "postgres"]

        for service in services:
            self.stdout.write(
                self.style.SUCCESS(f"Checking connection for {service}...")
            )
            if service == "neo4j":
                self.verify_neo4j_connection(debug)
            elif service == "redis":
                self.verify_redis_connection(debug)
            elif service == "postgres":
                self.verify_postgres_connection(debug)
            else:
                self.stdout.write(self.style.ERROR(f"Unknown service: {service}"))
            self.stdout.write("---")

    def verify_neo4j_connection(self, debug):
        NEO4J_USERNAME = env_config("NEO4J_USERNAME", default="neo4j")
        NEO4J_PASSWORD = env_config("NEO4J_PASSWORD", default="password")
        NEO4J_HOST = env_config("NEO4J_HOST", default="db-neo4j")
        NEO4J_PORT = env_config("NEO4J_PORT", default="7687")
        NEOMODEL_NEO4J_BOLT_URL = (
            f"bolt://{NEO4J_USERNAME}:{NEO4J_PASSWORD}@{NEO4J_HOST}:{NEO4J_PORT}"
        )

        config.DATABASE_URL = NEOMODEL_NEO4J_BOLT_URL

        if debug:
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mNEO4J_USERNAME: {NEO4J_USERNAME}\033[0m")
            )
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mNEO4J_PASSWORD: {NEO4J_PASSWORD}\033[0m")
            )
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mNEO4J_HOST: {NEO4J_HOST}\033[0m")
            )
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mNEO4J_PORT: {NEO4J_PORT}\033[0m")
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"\033[94mNEOMODEL_NEO4J_BOLT_URL: {NEOMODEL_NEO4J_BOLT_URL}\033[0m"
                )
            )

        try:
            db.cypher_query("MATCH (n) RETURN n LIMIT 1")
            self.stdout.write(self.style.SUCCESS("Connection to Neo4j successful!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Connection to Neo4j failed: {e}"))

    def verify_redis_connection(self, debug):
        REDIS_PASSWORD = env_config("REDIS_PASSWORD", default="")
        REDIS_HOST = env_config("REDIS_HOST", default="redis-service")
        REDIS_PORT = env_config("REDIS_PORT", default="6379")
        if REDIS_PASSWORD:
            CELERY_BROKER_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"
        else:
            CELERY_BROKER_URL = env_config(
                "CELERY_BROKER_URL", default="redis://redis:6379/0"
            )

        app = Celery("tasks", broker=CELERY_BROKER_URL)

        if debug:
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mREDIS_PASSWORD: {REDIS_PASSWORD}\033[0m")
            )
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mREDIS_HOST: {REDIS_HOST}\033[0m")
            )
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mREDIS_PORT: {REDIS_PORT}\033[0m")
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"\033[94mCELERY_BROKER_URL: {CELERY_BROKER_URL}\033[0m"
                )
            )

        try:
            app.connection().connect()
            self.stdout.write(self.style.SUCCESS("Connection to Redis successful!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Connection to Redis failed: {e}"))

    def verify_postgres_connection(self, debug):
        POSTGRES_DB = env_config("POSTGRES_DB", default="mediabedb")
        POSTGRES_USER = env_config("POSTGRES_USER", default="mediabeuser")
        POSTGRES_PASSWORD = env_config("POSTGRES_PASSWORD", default="mediabepassword")
        POSTGRES_HOST = env_config("POSTGRES_HOST", default="db-postgres")
        POSTGRES_PORT = env_config("POSTGRES_PORT", default="5432")

        db_conn = connections["default"]

        if debug:
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mPOSTGRES_DB: {POSTGRES_DB}\033[0m")
            )
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mPOSTGRES_USER: {POSTGRES_USER}\033[0m")
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"\033[94mPOSTGRES_PASSWORD: {POSTGRES_PASSWORD}\033[0m"
                )
            )
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mPOSTGRES_HOST: {POSTGRES_HOST}\033[0m")
            )
            self.stdout.write(
                self.style.SUCCESS(f"\033[94mPOSTGRES_PORT: {POSTGRES_PORT}\033[0m")
            )

        try:
            db_conn.cursor()
            self.stdout.write(
                self.style.SUCCESS("Connection to PostgreSQL successful!")
            )
        except OperationalError as e:
            self.stdout.write(self.style.ERROR(f"Connection to PostgreSQL failed: {e}"))


# Usage:
# python manage.py verify_connection -s all
# python manage.py verify_connection --services all
# python manage.py verify_connection -s neo4j redis postgres
# python manage.py verify_connection --services neo4j redis postgres
# python manage.py verify_connection (will default to all services)
# python manage.py verify_connection -d (will show detailed debug information)
