from django.utils import timezone
from managekit.utils.base_seed import BaseSeed
from .models import MessageTemplate


class MessageTemplateSeed(BaseSeed):
    raw_file = "message_templates"
    model = MessageTemplate

    @classmethod
    def get_fields(cls, item):
        # Use timezone-aware datetime
        current_time = timezone.now().isoformat()
        return {
            "message_type": item["message_type"],
            "code": item["code"],
            "description": item["description"],
            "subject": item["subject"],
            "body": item["body"],
            "user": item["user"],
            "variables": item["variables"],
            "created_at": current_time,
            "updated_at": current_time,
        }
