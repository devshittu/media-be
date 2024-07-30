import logging
from rest_framework import serializers
from .models import MessageTemplate

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class MessageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageTemplate
        fields = '__all__'

    def create(self, validated_data):
        logger.debug('Creating a new MessageTemplate instance')
        try:
            instance = super().create(validated_data)
            logger.info(
                f"MessageTemplate instance created with id {instance.id}")
            return instance
        except Exception as e:
            logger.error(f"Error creating MessageTemplate instance: {e}")
            raise

    def update(self, instance, validated_data):
        logger.debug(
            f'Updating MessageTemplate instance with id {instance.id}')
        try:
            instance = super().update(instance, validated_data)
            logger.info(
                f"MessageTemplate instance with id {instance.id} updated")
            return instance
        except Exception as e:
            logger.error(
                f"Error updating MessageTemplate instance with id {instance.id}: {e}")
            raise

# system_messaging/serializers.py
