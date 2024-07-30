import logging
from rest_framework import viewsets
from .models import MessageTemplate
from .serializers import MessageTemplateSerializer

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class MessageTemplateViewSet(viewsets.ModelViewSet):
    queryset = MessageTemplate.objects.all()
    serializer_class = MessageTemplateSerializer

    def list(self, request, *args, **kwargs):
        logger.debug('Listing all message templates')
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.debug(f"Retrieving message template with id {kwargs['pk']}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.debug('Creating a new message template')
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.debug(f"Updating message template with id {kwargs['pk']}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.debug(
            f"Partially updating message template with id {kwargs['pk']}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.debug(f"Deleting message template with id {kwargs['pk']}")
        return super().destroy(request, *args, **kwargs)
# system_messaging/views.py
