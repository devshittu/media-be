import logging
from rest_framework import serializers
from utils.serializers import UnixTimestampModelSerializer
from .models import (
    StoryInteraction,
    StoryInteractionMetadataSchema,
    AccessibilityTool,
    UserNotInterested,
    UserSession,
)
# from jsonschema import validate, ValidationError
from authentication.models import CustomUser

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class ViewMetadataSerializer(serializers.Serializer):
    source_page = serializers.CharField()

    def validate(self, data):
        logger.debug(f'Validating view metadata: {data}')
        return data


class BookmarkMetadataSerializer(serializers.Serializer):
    source_page = serializers.CharField()

    def validate(self, data):
        logger.debug(f'Validating bookmark metadata: {data}')
        return data


class ShareMetadataSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(
        choices=["WhatsApp", "Twitter", "Facebook", "Other"]
    )

    def validate(self, data):
        logger.debug(f'Validating share metadata: {data}')
        return data


class ClickExternalMetadataSerializer(serializers.Serializer):
    link_url = serializers.URLField()

    def validate(self, data):
        logger.debug(f'Validating click external metadata: {data}')
        return data


class ViewStorylineMetadataSerializer(serializers.Serializer):
    source_section = serializers.CharField()

    def validate(self, data):
        logger.debug(f'Validating view storyline metadata: {data}')
        return data


class AccessibilityToolSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = AccessibilityTool
        fields = "__all__"

    def validate(self, data):
        logger.debug(f'Validating accessibility tool data: {data}')
        return data


class StoryInteractionSerializer(UnixTimestampModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,  # The user field is not required
        allow_null=True,  # Allow null values
    )

    class Meta:
        model = StoryInteraction
        fields = [
            "id",
            "user",
            "story",
            "interaction_type",
            "created_at",
            "metadata",
        ]

    def validate(self, data):
        logger.debug(f'Validating story interaction data: {data}')
        # interaction_type = data.get("interaction_type")
        # metadata = data.get("metadata", {})
        # version = metadata.get("version", "2.0")

        # try:
        #     schema_record = StoryInteractionMetadataSchema.objects.get(
        #         interaction_type=interaction_type, version=version
        #     )
        #     schema = schema_record.schema
        #     validate(metadata, schema)
        #     logger.info(
        #         f'Successfully validated metadata for interaction type {interaction_type}')
        # except StoryInteractionMetadataSchema.DoesNotExist:
        #     logger.error(
        #         f'Schema not found for interaction type {interaction_type} and version {version}')
        #     raise serializers.ValidationError(
        #         f"Schema not found for interaction type '{interaction_type}' and version '{version}'.")
        # except ValidationError as e:
        #     logger.error(f'Invalid metadata: {str(e)}')
        #     raise serializers.ValidationError(f"Invalid metadata: {str(e)}")

        return data

    def create(self, validated_data):
        logger.debug(f'Creating story interaction with data: {validated_data}')
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["user"] = request.user
        interaction = super().create(validated_data)
        logger.info(
            f'Successfully created story interaction with id: {interaction.id}')
        return interaction


class UserNotInterestedSerializer(UnixTimestampModelSerializer):
    """
    Serializer for the UserNotInterested model.
    This serializer provides a representation of the data for stories users are not interested in.
    """

    user = serializers.ReadOnlyField(
        source="user.username"
    )  # Display the username of the user

    class Meta:
        model = UserNotInterested
        fields = ["id", "user", "story", "created_at", "reason"]

    # def validate(self, data):
    #     """
    #     Ensure that the user is not marking their own story as not interested.
    #     """
    #     if data['user'] == self.context['request'].user:
    #         raise serializers.ValidationError("You cannot mark your own story as not interested.")
    #     return data


class UserSessionSerializer(UnixTimestampModelSerializer):
    """
    Serializer for the UserSession model.
    This serializer provides a representation of a user's session, including associated device and location data.
    """

    user = serializers.ReadOnlyField(
        source="user.username"
    )  # Display the username of the user

    class Meta:
        model = UserSession
        fields = [
            "id",
            "user",
            "session_id",
            "device_data",
            "location_data",
            "start_timestamp" "device_type",
            "operating_system",
            "browser",
            "screen_resolution",
            "connection_type",
            "ip_address",
            "geolocation",
            "time_zone",
        ]

    def create(self, validated_data):
        """
        Override the create method to handle nested serializers.
        """
        logger.debug(f'Creating user session with data: {validated_data}')
        user_session = UserSession.objects.create(**validated_data)
        logger.info(
            f'Successfully created user session with id: {user_session.id}')
        return user_session


# analytics/serializers.py
