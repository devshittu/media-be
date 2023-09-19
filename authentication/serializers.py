from django.contrib.auth import get_user_model
from utils.serializers import UnixTimestampDateTimeField
from .models import CustomUser
from rest_framework import serializers


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'name',  'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            name=validated_data['name'],
            username=validated_data.get('username', None) or f"user_{validated_data['email'].split('@')[0]}"
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# class CustomUserSerializer(UnixTimestampDateTimeField):
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'name', 'email', 'username', 'avatar_url', 'display_picture',
            'date_of_birth', 'bio', 'phone_number', 'last_activity', 'roles',
            'is_active', 'is_staff', 'has_completed_setup'
        ]

# authentication/serializers.py