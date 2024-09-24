# from django.core.management.base import BaseCommand
# from django.conf import settings
# from elasticsearch import Elasticsearch, ElasticsearchException
# from elasticsearch.connection import RequestsHttpConnection
# import sys


# class Command(BaseCommand):
#     help = 'Checks if Elasticsearch is ready'

#     def handle(self, *args, **options):
#         es_settings = settings.ELASTICSEARCH_DSL['default']
#         es_hosts = es_settings['hosts']
#         http_auth = es_settings.get('http_auth', None)
#         use_ssl = es_settings.get('use_ssl', False)
#         verify_certs = es_settings.get('verify_certs', True)

#         try:
#             # Set up Elasticsearch client with proper connection class and auth
#             es = Elasticsearch(
#                 es_hosts,
#                 http_auth=http_auth,
#                 use_ssl=use_ssl,
#                 verify_certs=verify_certs,
#                 ca_certs=es_settings.get('ca_certs'),
#                 connection_class=RequestsHttpConnection,
#                 timeout=30
#             )

#             # Attempt to get cluster health
#             health = es.cluster.health()
#             status = health['status']
#             if status in ['green', 'yellow']:
#                 self.stdout.write(self.style.SUCCESS(
#                     f"Elasticsearch is ready with status: {status}"))
#                 sys.exit(0)
#             else:
#                 self.stdout.write(self.style.WARNING(
#                     f"Elasticsearch is not ready. Status: {status}"))
#                 sys.exit(1)
#         except ElasticsearchException as e:
#             self.stdout.write(self.style.ERROR(
#                 f"Error connecting to Elasticsearch: {e}"))
#             sys.exit(1)


# managekit/management/commands/check_elasticsearch.py

import sys
import warnings
from elasticsearch import Elasticsearch, ElasticsearchException
from django.conf import settings
from django.core.management.base import BaseCommand
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the InsecureRequestWarning from urllib3
warnings.filterwarnings('ignore', category=InsecureRequestWarning)


class Command(BaseCommand):
    help = 'Checks if Elasticsearch is ready'

    def handle(self, *args, **options):
        es_settings = settings.ELASTICSEARCH_DSL['default']
        es_hosts = es_settings['hosts']
        http_auth = es_settings.get('http_auth', None)
        use_ssl = es_settings.get('use_ssl', False)
        verify_certs = es_settings.get('verify_certs', True)
        ca_certs = es_settings.get('ca_certs', None)

        try:
            es = Elasticsearch(
                [es_hosts],
                http_auth=http_auth,
                use_ssl=use_ssl,
                verify_certs=verify_certs,
                ca_certs=ca_certs,
                timeout=30,
            )

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


# # python manage.py check_elasticsearch