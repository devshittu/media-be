from rest_framework import serializers
from utils.serializers import UnixTimestampDateTimeField
from .models import (
    StoryInteraction, DeviceData, LocationData, 
    ReferralData, AccessibilityTool, UserNotInterested, UserSession
)

class ViewMetadataSerializer(serializers.Serializer):
    source_page = serializers.CharField()

class BookmarkMetadataSerializer(serializers.Serializer):
    source_page = serializers.CharField()

class ShareMetadataSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(choices=['WhatsApp', 'Twitter', 'Facebook', 'Other'])

class ClickExternalMetadataSerializer(serializers.Serializer):
    link_url = serializers.URLField()

class ViewTimelineMetadataSerializer(serializers.Serializer):
    source_section = serializers.CharField()

# ... add more metadata serializers as needed ...


class DeviceDataSerializer(UnixTimestampDateTimeField):
    """
    Serializer for the DeviceData model.
    This serializer provides a representation of the device data associated with a user's session.
    """
    class Meta:
        model = DeviceData
        fields = ['device_type', 'operating_system', 'browser', 'screen_resolution', 'connection_type']


class LocationDataSerializer(UnixTimestampDateTimeField):
    """
    Serializer for the LocationData model.
    This serializer provides a representation of the location data associated with a user's session.
    """
    class Meta:
        model = LocationData
        fields = ['ip_address', 'geolocation', 'time_zone']


class ReferralDataSerializer(UnixTimestampDateTimeField):
    class Meta:
        model = ReferralData
        fields = '__all__'

class AccessibilityToolSerializer(UnixTimestampDateTimeField):
    class Meta:
        model = AccessibilityTool
        fields = '__all__'

class StoryInteractionSerializer(UnixTimestampDateTimeField):
    device_data = DeviceDataSerializer()
    location_data = LocationDataSerializer()
    referral_data = ReferralDataSerializer()

    class Meta:
        model = StoryInteraction
        fields = ['id', 'user', 'story', 'interaction_type', 'timestamp', 'metadata', 'device_data', 'location_data', 'referral_data']


    def validate(self, data):
        interaction_type = data.get('interaction_type')
        metadata = data.get('metadata', {})

        # Map interaction types to their respective metadata serializers
        metadata_serializers = {
            'view': ViewMetadataSerializer,
            'bookmark': BookmarkMetadataSerializer,
            'share': ShareMetadataSerializer,
            'click_external': ClickExternalMetadataSerializer,
            'view_timeline': ViewTimelineMetadataSerializer,
            # ... add more mappings as needed ...
        }

        # Get the appropriate serializer for the interaction type
        metadata_serializer_class = metadata_serializers.get(interaction_type)

        if metadata_serializer_class:
            metadata_serializer = metadata_serializer_class(data=metadata)
            if not metadata_serializer.is_valid():
                raise serializers.ValidationError({"metadata": metadata_serializer.errors})

        return data
    


class UserNotInterestedSerializer(UnixTimestampDateTimeField):
    """
    Serializer for the UserNotInterested model.
    This serializer provides a representation of the data for stories users are not interested in.
    """
    user = serializers.ReadOnlyField(source='user.username')  # Display the username of the user

    class Meta:
        model = UserNotInterested
        fields = ['id', 'user', 'story', 'timestamp', 'reason']

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
    device_data = DeviceDataSerializer()  # Nested serializer for device data
    location_data = LocationDataSerializer()  # Nested serializer for location data

    class Meta:
        model = UserSession
        fields = ['id', 'user', 'session_id', 'device_data', 'location_data', 'start_timestamp']

    def create(self, validated_data):
        """
        Override the create method to handle nested serializers.
        """
        device_data_data = validated_data.pop('device_data')
        location_data_data = validated_data.pop('location_data')

        device_data = DeviceData.objects.create(**device_data_data)
        location_data = LocationData.objects.create(**location_data_data)

        user_session = UserSession.objects.create(device_data=device_data, location_data=location_data, **validated_data)
        return user_session


# analytics/serializers.py