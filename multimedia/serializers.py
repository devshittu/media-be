import logging
from rest_framework import serializers
from .models import Multimedia

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class MultimediaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Multimedia model.
    """

    # user = serializers.ReadOnlyField(source="user.email")  # Display the user's email
    # user = serializers. (source="user.email", write_only=True)  # Display the user's email

    class Meta:
        model = Multimedia
        fields = [
            "file",
            "media_url",
            "caption",
            "thumbnail",
            "media_type",
            "id",
            "user",
            "story",
        ]

    def to_representation(self, instance):
        """
        Convert `Multimedia` instance to a dictionary representation.
        """
        logger.debug(f'Serializing multimedia instance {instance.id}')
        representation = super().to_representation(instance)
        logger.info(
            f'Multimedia instance {instance.id} serialized successfully')
        return representation

    def validate(self, attrs):
        """
        Validate the incoming data for the `Multimedia` instance.
        """
        logger.debug(f'Validating multimedia data: {attrs}')
        validated_data = super().validate(attrs)
        logger.info(f'Multimedia data validated successfully: {attrs}')
        return validated_data

    def create(self, validated_data):
        """
        Create a new `Multimedia` instance.
        """
        logger.debug(
            f'Creating multimedia instance with data: {validated_data}')
        multimedia_instance = super().create(validated_data)
        logger.info(
            f'Multimedia instance {multimedia_instance.id} created successfully')
        return multimedia_instance

    def update(self, instance, validated_data):
        """
        Update an existing `Multimedia` instance.
        """
        logger.debug(
            f'Updating multimedia instance {instance.id} with data: {validated_data}')
        multimedia_instance = super().update(instance, validated_data)
        logger.info(
            f'Multimedia instance {multimedia_instance.id} updated successfully')
        return multimedia_instance

# multimedia/serializers.py
