import logging
from .models import MessageTemplate
# from django.core.mail import send_mail
from .sendgrid_utils import send_email_via_sendgrid
from .twilio_utils import send_sms_via_twilio

logger = logging.getLogger('app_logger')


def send_sms(recipient, message):
    """Send an SMS via Twilio."""
    logger.debug(f'Preparing to send SMS to {recipient}')
    return send_sms_via_twilio(recipient, message)


def send_message(template_code, context, recipient):
    """
    Send a message using the specified template.

    Args:
        template_code (str): The code identifying the message template.
        context (dict): The context to replace placeholders in the template.
        recipient (str): The recipient's email address or phone number.

    Returns:
        None
    """
    logger.debug(f'Attempting to retrieve template with code {template_code}')
    try:
        template = MessageTemplate.objects.get(code=template_code)
        logger.info(f"Retrieved template for code {template_code}")
    except MessageTemplate.DoesNotExist:
        logger.error(
            f"Message template with code {template_code} does not exist.")
        return

    required_variables = template.variables.split(",")
    missing_variables = [
        var for var in required_variables if var not in context]

    if missing_variables:
        logger.error(
            f"Error sending message: Missing context variables: {', '.join(missing_variables)}"
        )
        return

    logger.debug('Replacing placeholders in the template')
    subject, message = template.replace_placeholders(context)

    if template.message_type == "email":
        logger.debug('Sending email via SendGrid')
        status, body, headers = send_email_via_sendgrid(
            subject, message, recipient)
        if status:
            logger.info(f"Email sent to {recipient} with status {status}")
        else:
            logger.error(f"Failed to send email to {recipient}")
    elif template.message_type == "sms":
        logger.debug('Sending SMS via Twilio')
        sid = send_sms(recipient, message)
        if sid:
            logger.info(f"SMS sent to {recipient} with SID {sid}")
        else:
            logger.error(f"Failed to send SMS to {recipient}")


# system_messaging/utils.py
