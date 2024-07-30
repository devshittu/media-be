import logging
from django.db import models
from django.conf import settings
from jinja2.sandbox import SandboxedEnvironment
from utils.models import SoftDeletableModel, TimestampedModel

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class MessageTemplate(SoftDeletableModel, TimestampedModel):
    MESSAGE_TYPES = (
        ("email", "Email"),
        ("sms", "Short Messaging Service"),
    )

    message_type = models.CharField(
        max_length=5, choices=MESSAGE_TYPES, default="email"
    )
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    # SMS might not need a subject
    subject = models.TextField(blank=True, null=True)
    body = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    variables = models.TextField(
        help_text="Comma separated list of expected variables")

    class Meta:
        verbose_name = "Message Template"
        verbose_name_plural = "Message Templates"

    def replace_placeholders(self, context):
        """Render email body and subject using Jinja2 from database content with sandboxing."""
        logger.debug(f"Rendering placeholders for template {self.code}")

        jinja_env = SandboxedEnvironment()

        # Extract templates from the database and render them with Jinja2

        try:
            template_body = jinja_env.from_string(self.body)
            rendered_body = template_body.render(**context)
            logger.debug(f"Rendered body for template {self.code}")

            template_subject = jinja_env.from_string(self.subject)
            rendered_subject = template_subject.render(**context)
            logger.debug(f"Rendered subject for template {self.code}")

            return rendered_subject, rendered_body
        except Exception as e:
            logger.error(f"Error rendering template {self.code}: {e}")
            raise

    def save(self, *args, **kwargs):
        logger.debug(f"Saving message template {self.code}")
        super().save(*args, **kwargs)
        logger.info(f"Saved message template {self.code}")

    def delete(self, *args, **kwargs):
        logger.debug(f"Deleting message template {self.code}")
        super().delete(*args, **kwargs)
        logger.info(f"Deleted message template {self.code}")

    def __str__(self):
        return f"Template {self.code} for {self.message_type} by {self.user.email}"

# system_messaging/models.py
