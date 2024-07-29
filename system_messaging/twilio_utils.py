import logging
from twilio.rest import Client
from django.conf import settings

logger = logging.getLogger('app_logger')


def send_sms_via_twilio(recipient, message):
    """
    Send an SMS via Twilio.

    Parameters:
        recipient (str): The phone number to send the SMS to.
        message (str): The message to be sent.

    Returns:
        str: The SID of the sent message if successful, None otherwise.
    """
    logger.debug("Starting send_sms_via_twilio function.")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    logger.debug("Twilio client initialized.")

    try:
        message = client.messages.create(
            to=recipient,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=message
        )
        logger.info(f"SMS sent to {recipient} with SID {message.sid}")
        return message.sid
    except Exception as e:
        logger.error(f"Error sending SMS to {recipient}: {e}")
        return None
    finally:
        logger.debug("Ending send_sms_via_twilio function.")

# system_messaging/twilio_utils.py
