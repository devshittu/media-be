from django.contrib.auth import get_user_model
from rest_framework import serializers


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'name', 'email', 'username', 'avatar_url', 'display_picture',
            # 'date_of_birth', 
            'bio', 
            'phone_number', 
            'last_activity', 
            'roles',
            'is_active', 'is_staff', 'has_completed_setup',
        ]


class AuthUserSerializer(serializers.ModelSerializer):
    settings = serializers.SerializerMethodField()
    feed_position = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'id', 'name', 'email', 'username', 'avatar_url', 'display_picture',
            # 'date_of_birth', 
            'bio', 
            'phone_number', 
            'last_activity', 
            'roles',
            'is_active', 'is_staff', 'has_completed_setup',
            'settings', 'feed_position'
        ]

    def get_settings(self, obj):
        # Lazy import inside the method
        from users.serializers import UserSettingSerializer
        return UserSettingSerializer(obj.settings).data

    def get_feed_position(self, obj):
        # Lazy import inside the method
        from users.serializers import UserFeedPositionSerializer
        return UserFeedPositionSerializer(obj.userfeedposition).data


# common/serializers.py