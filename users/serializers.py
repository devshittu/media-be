from rest_framework import serializers
from .models import Follow, UserSetting, UserFeedPosition
from utils.serializers import UnixTimestampModelSerializer
from common.serializers import CustomUserSerializer


class NotificationSettingsDataSerializer(serializers.Serializer):
    account = serializers.BooleanField(required=False)
    marketing = serializers.BooleanField(required=False)
    updates = serializers.BooleanField(required=False)


class SettingNotificationSerializer(serializers.Serializer):
    email = NotificationSettingsDataSerializer(required=False)


class AccountSettingsDataSerializer(serializers.Serializer):
    display_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)


class SystemSettingsDataSerializer(serializers.Serializer):
    theme = serializers.CharField(required=False)
    language = serializers.CharField(required=False)


class PersonalSettingsDataSerializer(serializers.Serializer):
    favorite_categories = serializers.ListField(
        child=serializers.CharField(), required=False
    )


class UserSettingSerializer(UnixTimestampModelSerializer):
    user_id = serializers.UUIDField(read_only=True)
    system_settings = SystemSettingsDataSerializer()
    account_settings = AccountSettingsDataSerializer()
    notification_settings = SettingNotificationSerializer()
    personal_settings = PersonalSettingsDataSerializer()

    class Meta:
        model = UserSetting
        fields = "__all__"

    def validate_settings_data(data):
        serializer = UserSettingSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            return serializer.validated_data
        return None

    def update(self, instance, validated_data):
        # Extract nested settings data
        personal_settings_data = validated_data.get("personal_settings", {})

        print("Current personal_settings:", instance.personal_settings)
        print("Incoming personal_settings_data:", personal_settings_data)

        # Merge old and new data for personal settings
        instance.personal_settings = {
            **instance.personal_settings,
            **personal_settings_data,
        }

        print("Merged personal_settings:", instance.personal_settings)

        # Extract nested settings data
        # personal_settings_data = validated_data.get('personal_settings', {})
        system_settings_data = validated_data.get("system_settings", {})
        account_settings_data = validated_data.get("account_settings", {})
        notification_settings_data = validated_data.get("notification_settings", {})

        print("Current notification_settings:", instance.notification_settings)
        print("Incoming notification_settings_data:", notification_settings_data)

        # Merge old and new data for each setting
        # instance.personal_settings = {**instance.personal_settings, **personal_settings_data}
        instance.system_settings = {**instance.system_settings, **system_settings_data}
        instance.account_settings = {
            **instance.account_settings,
            **account_settings_data,
        }
        # instance.notification_settings = {**instance.notification_settings, **notification_settings_data}

        # Special handling for nested dictionary in notification settings
        email_settings_data = notification_settings_data.get("email", {})
        if "email" in instance.notification_settings:
            instance.notification_settings["email"] = {
                **instance.notification_settings["email"],
                **email_settings_data,
            }
        else:
            instance.notification_settings["email"] = email_settings_data

        print("Merged notification_settings:", instance.notification_settings)

        instance.save()

        return instance


class FollowSerializer(serializers.ModelSerializer):
    follower = CustomUserSerializer(read_only=True)
    followed = CustomUserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ("id", "follower", "followed")


class UserFeedPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedPosition
        fields = ["last_story_read"]


# users/serializers.py
