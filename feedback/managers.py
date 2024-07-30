import logging
from django.db import models

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class ReportManager(models.Manager):
    def unflagged(self):
        logger.debug('Retrieving unflagged reports')
        return self.filter(is_flagged=False)

    def flagged(self):
        logger.debug('Retrieving flagged reports')
        return self.filter(is_flagged=True)

# feedback/managers.py
