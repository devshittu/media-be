# UserFeedPosition
from django.utils import timezone
from managekit.utils.base_seed import BaseSeed
from .models import UserFeedPosition
from authentication.seeds import CustomUserSeed
from stories.seeds import StorySeed


class UserFeedPositionSeed(BaseSeed):
    raw_file = "user_feed_position"
    model = UserFeedPosition
    dependencies = [
        CustomUserSeed,
        StorySeed,
    ]

    @classmethod
    def get_fields(cls, item):
        # Use timezone-aware datetime
        current_time = timezone.now().isoformat()
        return {
            "user": item["user"],
            "last_story_read": item["last_story_read"],
            "created_at": current_time,
            "updated_at": current_time,
        }


# users/seeds.py
