import logging
from django.apps import AppConfig

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class SupportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'support'

    def ready(self):
        logger.debug('Support app is ready')

# support/apps.py
