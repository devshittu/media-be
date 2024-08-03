import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, VerificationToken, OTP
from .tasks import (
    send_welcome_email,
    send_link_verification_email,
    send_otp_verification_email,
)
from decouple import config
from django.conf import settings
from django.utils.crypto import get_random_string
from datetime import timedelta
from django.utils import timezone

# Set up the logger for this module
logger = logging.getLogger('app_logger')


@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to handle tasks after a user is created or updated.
    For instance, sending a welcome email, or updating related models.
    """
    if created:
        logger.info(f'New user created: {instance.id}')

        # Send a welcome email
        context = {
            "PlatformName": config("APP_NAME", default="App Name", cast=str),
            "UserName": instance.display_name,
        }
        try:
            # Trigger the Celery task
            send_welcome_email.delay(instance.id, context)
            logger.info(f'Welcome email sent to user {instance.id}')
        except Exception as e:
            logger.error(
                f'Failed to send welcome email to user {instance.id}: {e}')

        # Handle account verification method
        if settings.ACCOUNT_VERIFICATION_METHOD == "OTP":
            try:
                # Generate new OTP
                otp_code = get_random_string(
                    length=6, allowed_chars="0123456789")
                otp = OTP.objects.create(
                    user=instance,
                    otp=otp_code,
                    expires_at=timezone.now() + timedelta(minutes=10),  # OTP valid for 10 minutes
                )
                logger.debug(f'Generated OTP for user {instance.id}')

                # Send OTP to user's email
                context = {
                    "UserName": instance.display_name,
                    "OTP_CODE": otp.otp,
                    "PlatformName": config("APP_NAME", default="App Name", cast=str),
                }
                send_otp_verification_email.delay(
                    instance.id, context)  # Trigger the Celery task
                logger.info(f'OTP email sent to user {instance.id}')
            except Exception as e:
                logger.error(
                    f'Failed to generate or send OTP to user {instance.id}: {e}')

        elif settings.ACCOUNT_VERIFICATION_METHOD == "VERIFICATION_LINK":
            try:
                # Generate a verification token and save it
                token = get_random_string(length=32)
                verification_token = VerificationToken.objects.create(
                    user=instance,
                    token=token,
                    expires_at=timezone.now() + timedelta(hours=24),  # Token is valid for 24 hours
                )
                logger.debug(
                    f'Generated verification token for user {instance.id}')

                # Send an email to the user with the verification link
                verification_link = f"{config('APP_FRONTEND_DOMAIN', default='http://127.0.0.1:3000/', cast=str)}verify-account/{token}"

                context = {
                    "UserName": instance.display_name,
                    "VerificationLink": verification_link,
                    "PlatformName": config("APP_NAME", default="App Name", cast=str),
                }
                send_link_verification_email.delay(
                    instance.id, context)  # Trigger the Celery task
                logger.info(
                    f'Verification link email sent to user {instance.id}')
            except Exception as e:
                logger.error(
                    f'Failed to generate or send verification link to user {instance.id}: {e}')

    else:
        logger.info(f'User updated: {instance.id}')
        # Handle tasks when a user's details are updated.
        pass

# # authentication/signals.py
