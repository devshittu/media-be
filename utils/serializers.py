from django.db import models
from rest_framework.serializers import ModelSerializer
from .fields import UnixTimestampDateTimeField

class UnixTimestampModelSerializer(ModelSerializer):
    """
    A base serializer that represents DateTimeField as UNIX timestamps.
    """
    serializer_field_mapping = {
        **ModelSerializer.serializer_field_mapping,
        models.DateTimeField: UnixTimestampDateTimeField
    }
