import logging
from decouple import config
from celery import shared_task
# from system_messaging.utils import send_email_via_sendgrid
from system_messaging.utils import send_message
logger = logging.getLogger('app_logger')


@shared_task
def send_test_email(recipient):
    context = {
        "PlatformName": config("APP_NAME", default="App Name", cast=str),
        "UserName": recipient,
    }

    logger.debug(f'Sending test email to {recipient}')
    send_message('test_email', context, recipient)
    logger.info(f"Triggered test email to {recipient}")

# system_messaging/tasks.py
