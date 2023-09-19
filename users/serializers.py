from rest_framework import serializers
from .models import Follow, UserSetting
from authentication.serializers import CustomUserSerializer
from utils.serializers import UnixTimestampModelSerializer

class NotificationSettingsDataSerializer(serializers.Serializer):
    account = serializers.IntegerField()
    marketing = serializers.IntegerField()
    updates = serializers.IntegerField()

class SettingNotificationSerializer(serializers.Serializer):
    email = NotificationSettingsDataSerializer()

class AccountSettingsDataSerializer(serializers.Serializer):
    display_name = serializers.CharField()
    email = serializers.EmailField()

class SystemSettingsDataSerializer(serializers.Serializer):
    theme = serializers.CharField()
    language = serializers.CharField()

class PersonalSettingsDataSerializer(serializers.Serializer):
    favorite_categories = serializers.ListField(child=serializers.CharField())

class UserSettingSerializer(UnixTimestampModelSerializer):
    user_id = serializers.UUIDField()
    system_settings = SystemSettingsDataSerializer()
    account_settings = AccountSettingsDataSerializer()
    notification_settings = SettingNotificationSerializer()
    personal_settings = PersonalSettingsDataSerializer()

    class Meta:
        model = UserSetting
        fields = '__all__'

    def validate_settings_data(data):
        serializer = UserSettingSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data
        return None

class FollowSerializer(serializers.ModelSerializer):
    follower = CustomUserSerializer(read_only=True)
    followed = CustomUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('id', 'follower', 'followed', 'timestamp')

# users/serializers.py
