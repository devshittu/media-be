import logging
from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Report
from utils.serializers import UnixTimestampModelSerializer

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class GenericReportSerializer(UnixTimestampModelSerializer):
    content_type_name = serializers.CharField(write_only=True)

    class Meta:
        model = Report
        fields = '__all__'
        extra_kwargs = {
            'content_type': {'read_only': True}
        }

    def validate_content_type_name(self, value):
        logger.debug(f'Validating content type name: {value}')
        try:
            return ContentType.objects.get(model=value.lower())
        except ContentType.DoesNotExist:
            logger.warning(f'No content type exists for model {value}')
            raise serializers.ValidationError(
                f"No content type exists for model {value}")
# feedback/serializers.py
