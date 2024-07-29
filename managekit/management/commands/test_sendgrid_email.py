from django.core.management.base import BaseCommand
from system_messaging.tasks import send_test_email


class Command(BaseCommand):
    help = "Test SendGrid email configuration"

    def add_arguments(self, parser):
        parser.add_argument('recipient', type=str,
                            help='The email address to send the test email to')

    def handle(self, *args, **kwargs):
        recipient = kwargs['recipient']
        send_test_email.delay(recipient)
        self.stdout.write(self.style.SUCCESS(
            f'Triggered test email to {recipient}'))

# python manage.py test_sendgrid_email devshittu@gmail.com
# managekit/management/commands/test_sendgrid_email.py
