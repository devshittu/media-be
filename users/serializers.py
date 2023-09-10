from rest_framework import serializers
from .models import User, Settings, Category

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'date_joined', 'preferred_categories', 'language', 'theme')

class SettingsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Settings model.
    """
    class Meta:
        model = Settings
        fields = ('user', 'preferred_categories', 'language', 'theme')
