from django.db import models
from jinja2.sandbox import SandboxedEnvironment


class MessageTemplate(models.Model):
    MESSAGE_TYPES = (
        ('email', 'Email'),
        ('sms', 'Short Messaging Service'),
    )

    message_type = models.CharField(max_length=5, choices=MESSAGE_TYPES, default='email')
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    subject = models.TextField(blank=True, null=True)  # SMS might not need a subject
    body = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    variables = models.TextField(help_text="Comma separated list of expected variables")

    
    def replace_placeholders(self, context):
        """Render email body and subject using Jinja2 from database content with sandboxing."""

        jinja_env = SandboxedEnvironment()

        # Extract templates from the database and render them with Jinja2
        template_body = jinja_env.from_string(self.body)
        rendered_body = template_body.render(**context)
        
        template_subject = jinja_env.from_string(self.subject)
        rendered_subject = template_subject.render(**context)
        
        return rendered_subject, rendered_body
