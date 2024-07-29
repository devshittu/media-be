from rest_framework import serializers
from .models import MessageTemplate


class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = '__all__'

# system_messaging/serializers.py
