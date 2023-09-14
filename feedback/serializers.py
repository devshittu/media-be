from rest_framework import serializers
from .models import Report

class GenericReportSerializer(serializers.ModelSerializer):
    """
    Serializer for the Report model.
    """
    class Meta:
        model = Report
        fields = '__all__'
