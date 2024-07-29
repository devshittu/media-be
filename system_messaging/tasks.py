from celery import shared_task
from system_messaging.utils import send_email_via_sendgrid
import logging

logger = logging.getLogger('app_logger')


@shared_task
def send_test_email(recipient):
    subject = "Test Email from SendGrid"
    message = "<p>This is a test email sent to verify the SendGrid email config.</p>"

    logger.debug(f'Sending test email to {recipient}')
    status, body, headers = send_email_via_sendgrid(
        subject, message, recipient)

    if status:
        logger.info(f"Test email sent to {recipient} with status {status}")
    else:
        logger.error(f"Failed to send test email to {recipient}")

# system_messaging/tasks.py
