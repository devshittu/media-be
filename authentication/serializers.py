from .models import CustomUser, VerificationToken
from rest_framework import serializers
# from common.serializers import CustomUserSerializer

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



class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)


class VerificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationToken
        fields = ('token',)


# authentication/serializers.py