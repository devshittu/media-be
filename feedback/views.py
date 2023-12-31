from rest_framework import generics
from django.contrib.contenttypes.models import ContentType
from .models import Report
from .serializers import GenericReportSerializer
from utils.mixins import ReportCreationMixin


class ReportCreateView(ReportCreationMixin, generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = GenericReportSerializer

    def perform_create(self, serializer):
        content_type = serializer.validated_data.pop('content_type_name', None)
        
        if self.request.user.is_authenticated and not serializer.validated_data.get('is_anonymous'):
            serializer.save(user=self.request.user, content_type=content_type)
        else:
            serializer.save(content_type=content_type)
        
        # Handle post report creation
        instance = serializer.instance
        self.handle_post_report_creation(instance.content_object)
