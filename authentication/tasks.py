import logging
from celery import shared_task
from .models import CustomUser
from system_messaging.utils import send_message

# Set up the logger for this module
logger = logging.getLogger('app_logger')


@shared_task
def send_welcome_email(user_id, context):
    logger.debug(f'Attempting to send welcome email to user {user_id}')
    try:
        user = CustomUser.objects.get(id=user_id)
        logger.info(f'User {user_id} retrieved for welcome email')
        send_message('welcome_email', context, user.email)
        logger.info(f'Welcome email sent to user {user_id}')
    except CustomUser.DoesNotExist:
        logger.error(
            f'User {user_id} does not exist, cannot send welcome email')
    except Exception as e:
        logger.error(f'Error sending welcome email to user {user_id}: {e}')


@shared_task
def send_otp_verification_email(user_id, context):
    logger.debug(
        f'Attempting to send OTP verification email to user {user_id}')
    try:
        user = CustomUser.objects.get(id=user_id)
        logger.info(f'User {user_id} retrieved for OTP verification email')
        send_message('otp_verification_email', context, user.email)
        logger.info(f'OTP verification email sent to user {user_id}')
    except CustomUser.DoesNotExist:
        logger.error(
            f'User {user_id} does not exist, cannot send OTP verification email')
    except Exception as e:
        logger.error(
            f'Error sending OTP verification email to user {user_id}: {e}')


@shared_task
def send_link_verification_email(user_id, context):
    logger.debug(
        f'Attempting to send link verification email to user {user_id}')
    try:
        user = CustomUser.objects.get(id=user_id)
        logger.info(f'User {user_id} retrieved for link verification email')
        send_message('link_verification_email', context, user.email)
        logger.info(f'Link verification email sent to user {user_id}')
    except CustomUser.DoesNotExist:
        logger.error(
            f'User {user_id} does not exist, cannot send link verification email')
    except Exception as e:
        logger.error(
            f'Error sending link verification email to user {user_id}: {e}')

# authentication/tasks.py
