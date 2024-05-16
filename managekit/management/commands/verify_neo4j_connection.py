from django.core.management.base import BaseCommand
from neomodel import config, db
from django.conf import settings


class Command(BaseCommand):
    help = "Verify connection to Neo4j database"

    def handle(self, *args, **kwargs):
        # Set the Neo4j connection URL
        config.DATABASE_URL = settings.NEOMODEL_NEO4J_BOLT_URL

        # Attempt to connect to the Neo4j database and run a test query
        try:
            db.cypher_query("MATCH (n) RETURN n LIMIT 1")
            self.stdout.write(self.style.SUCCESS("Connection to Neo4j successful!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Connection to Neo4j failed: {e}"))
