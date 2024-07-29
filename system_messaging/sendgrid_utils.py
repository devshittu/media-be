
import logging
import sendgrid
from sendgrid.helpers.mail import Mail
from django.conf import settings

# Set up the logger for this module
logger = logging.getLogger('app_logger')


def send_email_via_sendgrid(subject, message, recipient):
    """
    Send an email using SendGrid.

    Args:
        subject (str): The subject of the email.
        message (str): The body of the email.
        recipient (str): The recipient's email address.

    Returns:
        tuple: The status code, response body, and response headers.
               Returns (None, None, None) in case of an error.
    """
    logger.debug('Initializing SendGrid API client')
    sg = sendgrid.SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)

    logger.debug('Creating email object')
    email = Mail(
        from_email=settings.DEFAULT_FROM_EMAIL,
        to_emails=recipient,
        subject=subject,
        plain_text_content=message
    )

    try:
        logger.debug('Sending email')
        response = sg.send(email)

        logger.info(
            f"Email sent to {recipient} with status {response.status_code}"
        )
        return response.status_code, response.body, response.headers
    except Exception as e:
        logger.error(f"Error sending email to {recipient}: {e}")
        return None, None, None
