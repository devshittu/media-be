from rest_framework import serializers
from .models import User, Settings, Category

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'preferred_categories', 'language', 'theme')

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

class SettingSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()
    system_settings = SystemSettingsDataSerializer()
    account_settings = AccountSettingsDataSerializer()
    notification_settings = SettingNotificationSerializer()
    personal_settings = PersonalSettingsDataSerializer()
    last_updated = serializers.IntegerField()
    created_at = serializers.IntegerField()
    updated_at = serializers.IntegerField()


    def validate_settings_data(data):
        serializer = SettingSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data
        return None

# users/serializers.py
