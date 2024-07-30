import logging
from rest_framework import generics
from .models import Report
from .serializers import GenericReportSerializer
from utils.mixins import ReportCreationMixin

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class ReportCreateView(ReportCreationMixin, generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = GenericReportSerializer

    def perform_create(self, serializer):
        logger.debug('Performing create operation for a new report')
        content_type = serializer.validated_data.pop('content_type_name', None)

        if self.request.user.is_authenticated and not serializer.validated_data.get('is_anonymous'):
            serializer.save(user=self.request.user, content_type=content_type)
            logger.info(f'Report created by user {self.request.user}')
        else:
            serializer.save(content_type=content_type)
            logger.info('Report created anonymously')

        # Handle post report creation
        instance = serializer.instance
        self.handle_post_report_creation(instance.content_object)
        logger.debug('Handled post report creation')

# feedback/views.py
