from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from .models import Report
from utils.serializers import UnixTimestampModelSerializer

class GenericReportSerializer(UnixTimestampModelSerializer):
    content_type_name = serializers.CharField(write_only=True)

    class Meta:
        model = Report
        fields = '__all__'
        extra_kwargs = {
            'content_type': {'read_only': True}
        }

    def validate_content_type_name(self, value):
        try:
            return ContentType.objects.get(model=value.lower())
        except ContentType.DoesNotExist:
            raise serializers.ValidationError(f"No content type exists for model {value}")
