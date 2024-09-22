from django.core.management.base import BaseCommand
from django.conf import settings
from elasticsearch import Elasticsearch, ElasticsearchException
import sys


class Command(BaseCommand):
    help = 'Checks if Elasticsearch is ready'

    def handle(self, *args, **options):
        es_settings = settings.ELASTICSEARCH_DSL['default']
        es_hosts = es_settings['hosts']
        try:
            es = Elasticsearch(es_hosts, verify_certs=False, timeout=30)
            # Attempt to get cluster health
            health = es.cluster.health()
            status = health['status']
            if status in ['green', 'yellow']:
                self.stdout.write(self.style.SUCCESS(
                    f"Elasticsearch is ready with status: {status}"))
                sys.exit(0)
            else:
                self.stdout.write(self.style.WARNING(
                    f"Elasticsearch is not ready. Status: {status}"))
                sys.exit(1)
        except ElasticsearchException as e:
            self.stdout.write(self.style.ERROR(
                f"Error connecting to Elasticsearch: {e}"))
            sys.exit(1)


# python manage.py check_elasticsearch
