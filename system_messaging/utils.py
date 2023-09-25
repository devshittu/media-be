from .models import MessageTemplate
from django.core.mail import send_mail
from django.conf import settings
from .models import MessageTemplate

# from twilio.rest import Client


def send_sms(recipient, message):
    """Send an SMS via Twilio."""
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # client.messages.create(
    #     to=recipient,
    #     from_=settings.TWILIO_PHONE_NUMBER,
    #     body=message
    # )
    pass


def send_message(template_code, context, recipient):
    try:
        template = MessageTemplate.objects.get(code=template_code)
    except MessageTemplate.DoesNotExist:
        print(f"Message template with code {template_code} does not exist.")
        return

    required_variables = template.variables.split(",")
    missing_variables = [var for var in required_variables if var not in context]

    if missing_variables:
        print(
            f"Error sending message: Missing context variables: {', '.join(missing_variables)}"
        )
        return

    subject, message = template.replace_placeholders(context)

    if template.message_type == "email":
        send_mail(subject, message, "from_email@example.com", [recipient])
    elif template.message_type == "sms":
        send_sms(recipient, message)


# system_messaging/utils.py
