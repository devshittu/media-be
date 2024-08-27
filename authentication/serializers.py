from .models import CustomUser, VerificationToken, PasswordResetToken
from rest_framework import serializers
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
import logging

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class CustomUserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "display_name", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        logger.debug(f'Creating user with email: {validated_data["email"]}')
        user = CustomUser(
            email=validated_data["email"],
            display_name=validated_data["display_name"],
            username=validated_data.get("username", None)
            or f"user_{validated_data['email'].split('@')[0]}",
        )
        user.set_password(validated_data["password"])
        user.save()
        logger.info(f'User created with email: {user.email}')
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        logger.debug(f'Validating email for password reset: {value}')
        if not CustomUser.objects.filter(email=value).exists():
            logger.warning(
                f'Password reset requested for non-existent email: {value}')
            raise serializers.ValidationError(
                "This email address is not registered.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_token(self, value):
        logger.debug(f'Validating token for password reset: {value}')
        if not PasswordResetToken.objects.filter(token=value).exists():
            logger.warning(f'Invalid token for password reset: {value}')
            raise serializers.ValidationError("Invalid token.")
        return value

    def validate_password(self, value):
        logger.debug(f'Validating new password')
        password_validation.validate_password(value)
        return value

    def save(self, **kwargs):
        token = self.validated_data["token"]
        new_password = self.validated_data["password"]

        # Retrieve the user associated with the PasswordResetToken
        reset_token = PasswordResetToken.objects.get(token=token)
        user = reset_token.user

        # Set the new password for the user
        user.set_password(new_password)
        user.save()

        # Log the password reset action
        logger.info(f'Password reset for user: {user.email}')

        # Optionally, delete the used token to prevent reuse
        reset_token.delete()

        return user


class VerificationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = VerificationToken
        fields = ("token",)


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        logger.debug(f'Validating old password for user: {user.email}')
        if not user.check_password(value):
            logger.warning(f'Invalid old password for user: {user.email}')
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate(self, data):
        if data["new_password"] != data["confirm_new_password"]:
            logger.warning(
                f'Password mismatch for user: {self.context["request"].user.email}')
            raise serializers.ValidationError("New passwords must match")
        password_validation.validate_password(
            data["new_password"], self.context["request"].user
        )
        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        logger.debug(f'Updating password for user: {user.email}')
        user.password = make_password(self.validated_data["new_password"])
        user.save()
        logger.info(f'Password updated for user: {user.email}')
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "email", "display_name"]

    def validate_email(self, value):
        logger.debug(f'Validating email for update: {value}')
        if (
            CustomUser.objects.exclude(pk=self.instance.pk)
            .filter(email=value)
            .exists()
        ):
            logger.warning(f'Email {value} is already in use.')
            raise serializers.ValidationError("This email is already in use.")
        return value

    def validate_username(self, value):
        logger.debug(f'Validating username for update: {value}')
        if (
            CustomUser.objects.exclude(pk=self.instance.pk)
            .filter(username=value)
            .exists()
        ):
            logger.warning(f'Username {value} is already in use.')
            raise serializers.ValidationError(
                "This username is already in use.")
        return value


# authentication/serializers.py
