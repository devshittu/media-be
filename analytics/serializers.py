from rest_framework import serializers
from utils.serializers import UnixTimestampDateTimeField
from .models import (
    StoryInteraction, StoryInteractionMetadataSchema, AccessibilityTool, UserNotInterested, UserSession
)
from jsonschema import validate, ValidationError

class ViewMetadataSerializer(serializers.Serializer):
    source_page = serializers.CharField()

class BookmarkMetadataSerializer(serializers.Serializer):
    source_page = serializers.CharField()

class ShareMetadataSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(choices=['WhatsApp', 'Twitter', 'Facebook', 'Other'])

class ClickExternalMetadataSerializer(serializers.Serializer):
    link_url = serializers.URLField()

class ViewStorylineMetadataSerializer(serializers.Serializer):
    source_section = serializers.CharField()


class AccessibilityToolSerializer(UnixTimestampDateTimeField):
    class Meta:
        model = AccessibilityTool
        fields = '__all__'



class StoryInteractionSerializer(UnixTimestampDateTimeField):

    class Meta:
        model = StoryInteraction
        fields = ['id', 'user', 'story', 'interaction_type', 
                  'created_at', 'metadata', 'device_data', 
                  'location_data', 'referral_data']


    def validate(self, data):
        interaction_type = data.get('interaction_type')
        metadata = data.get('metadata', {})
        version = metadata.get('version')

        # Fetch the schema from the registry
        schema_record = StoryInteractionMetadataSchema.objects.get(interaction_type=interaction_type, version=version)
        schema = schema_record.schema

        # Validate metadata against the schema
        try:
            validate(metadata, schema)
        except ValidationError as e:
            raise serializers.ValidationError(f"Invalid metadata: {str(e)}")

        return data
        # # Map interaction types to their respective metadata serializers
        # metadata_serializers = {
        #     'view': ViewMetadataSerializer,
        #     'bookmark': BookmarkMetadataSerializer,
        #     'share': ShareMetadataSerializer,
        #     'click_external': ClickExternalMetadataSerializer,
        #     'view_storyline': ViewStorylineMetadataSerializer,
        #     # ... add more mappings as needed ...
        # }

        # # Get the appropriate serializer for the interaction type
        # metadata_serializer_class = metadata_serializers.get(interaction_type)

        # if metadata_serializer_class:
        #     metadata_serializer = metadata_serializer_class(data=metadata)
        #     if not metadata_serializer.is_valid():
        #         raise serializers.ValidationError({"metadata": metadata_serializer.errors})

        # return data
    


class UserNotInterestedSerializer(UnixTimestampDateTimeField):
    """
    Serializer for the UserNotInterested model.
    This serializer provides a representation of the data for stories users are not interested in.
    """
    user = serializers.ReadOnlyField(source='user.username')  # Display the username of the user

    class Meta:
        model = UserNotInterested
        fields = ['id', 'user', 'story', 'created_at', 'reason']

    # def validate(self, data):
    #     """
    #     Ensure that the user is not marking their own story as not interested.
    #     """
    #     if data['user'] == self.context['request'].user:
    #         raise serializers.ValidationError("You cannot mark your own story as not interested.")
    #     return data




class UserSessionSerializer(UnixTimestampDateTimeField):
    """
    Serializer for the UserSession model.
    This serializer provides a representation of a user's session, including associated device and location data.
    """
    user = serializers.ReadOnlyField(source='user.username')  # Display the username of the user

    class Meta:
        model = UserSession
        fields = ['id', 'user', 'session_id', 'device_data', 'location_data', 'start_timestamp'
                  'device_type', 'operating_system', 'browser', 'screen_resolution', 'connection_type',
                  'ip_address', 'geolocation', 'time_zone']

    def create(self, validated_data):
        """
        Override the create method to handle nested serializers.
        """
        user_session = UserSession.objects.create( **validated_data)
        return user_session


# analytics/serializers.py