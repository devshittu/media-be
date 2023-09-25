from celery import shared_task
from .models import CustomUser
from system_messaging.utils import send_message

@shared_task
def send_welcome_email(user_id, context):
    user = CustomUser.objects.get(id=user_id)
    # Assuming you have a send_message function that sends emails
    send_message('welcome_email', context, user.email)

@shared_task
def send_otp_verification_email(user_id, context):
    user = CustomUser.objects.get(id=user_id)
    # Assuming you have a send_message function that sends emails
    send_message('otp_verification_email', context, user.email)

@shared_task
def send_link_verification_email(user_id, context):
    user = CustomUser.objects.get(id=user_id)
    # Assuming you have a send_message function that sends emails
    send_message('link_verification_email', context, user.email)

# authentication/tasks.py