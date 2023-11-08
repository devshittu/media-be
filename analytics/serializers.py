from rest_framework import serializers
from utils.serializers import UnixTimestampModelSerializer
from .models import (
    StoryInteraction,
    StoryInteractionMetadataSchema,
    AccessibilityTool,
    UserNotInterested,
    UserSession,
)
from jsonschema import validate, ValidationError
from authentication.models import CustomUser


class ViewMetadataSerializer(serializers.Serializer):
    source_page = serializers.CharField()


class BookmarkMetadataSerializer(serializers.Serializer):
    source_page = serializers.CharField()


class ShareMetadataSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(
        choices=["WhatsApp", "Twitter", "Facebook", "Other"]
    )


class ClickExternalMetadataSerializer(serializers.Serializer):
    link_url = serializers.URLField()


class ViewStorylineMetadataSerializer(serializers.Serializer):
    source_section = serializers.CharField()


class AccessibilityToolSerializer(UnixTimestampModelSerializer):
    class Meta:
        model = AccessibilityTool
        fields = "__all__"


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
        # interaction_type = data.get("interaction_type")
        # metadata = data.get("metadata", {})
        # version = metadata.get(
        #     "version", "2.0"
        # )  # Provide a default version if not specified

        # # Fetch the schema from the registry
        # try:
        #     schema_record = StoryInteractionMetadataSchema.objects.get(
        #         interaction_type=interaction_type, version=version
        #     )
        # except StoryInteractionMetadataSchema.DoesNotExist:
        #     raise serializers.ValidationError(
        #         f"Schema not found for interaction type '{interaction_type}' and version '{version}'."
        #     )

        # schema = schema_record.schema

        # # Validate metadata against the schema
        # try:
        #     validate(metadata, schema)
        # except ValidationError as e:
        #     raise serializers.ValidationError(f"Invalid metadata: {str(e)}")

        return data

    def create(self, validated_data):
        # If the user is authenticated, add them to the validated_data
        request = self.context.get("request")
        if request and hasattr(request, "user") and request.user.is_authenticated:
            validated_data["user"] = request.user
        return super().create(validated_data)


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
        user_session = UserSession.objects.create(**validated_data)
        return user_session


# analytics/serializers.py
