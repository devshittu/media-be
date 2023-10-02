from django.utils import timezone
from managekit.utils.base_seed import BaseSeed
from .models import (
    StoryInteraction,
    StoryInteractionMetadataSchema,
    UserNotInterested,
    AccessibilityTool,
    UserSession,
)
from authentication.seeds import CustomUserSeed
from stories.seeds import StorySeed
from django.core.exceptions import ObjectDoesNotExist


class StoryInteractionMetadataSchemaSeed(BaseSeed):
    raw_file = "story_interaction_metadata_schemas"
    model = StoryInteractionMetadataSchema

    @classmethod
    def get_fields(cls, item):
        # Use timezone-aware datetime
        current_time = timezone.now().isoformat()
        return {
            "interaction_type": item["interaction_type"],
            "version": item["version"],
            "schema": item["schema"],
            "created_at": current_time,
            "updated_at": current_time,
        }


class UserSessionSeed(BaseSeed):
    raw_file = "user_sessions"
    model = UserSession
    dependencies = [
        CustomUserSeed,
    ]
    pk_field = "session_token"  # Set session_token as the primary key field

    @classmethod
    def get_fields(cls, item):
        current_time = timezone.now().isoformat()
        return {
            "user": item["user"],
            "session_token": item[
                "session_token"
            ],  # Use session_token as the primary key
            "device_type": item["device_type"],
            "operating_system": item["operating_system"],
            "browser": item["browser"],
            "screen_resolution": item["screen_resolution"],
            "connection_type": item["connection_type"],
            "ip_address": item["ip_address"],
            "geolocation": item["geolocation"],
            "time_zone": item["time_zone"],
            "start_timestamp": item["start_timestamp"],
            "created_at": current_time,
            "updated_at": current_time,
        }


class StoryInteractionSeed(BaseSeed):
    raw_file = "story_interactions"
    model = StoryInteraction
    dependencies = [
        CustomUserSeed,
        StorySeed,
    ]

    @classmethod
    def get_fields(cls, item):
        current_time = timezone.now().isoformat()
        session = None
        try:
            session = UserSession.objects.get(session_token=item["session_token"])
        except ObjectDoesNotExist:
            print(f"Session with token {item['session_token']} not found!")
            return None

        return {
            "user": item["user"],
            "story": item["story"],
            "interaction_type": item["interaction_type"],
            "metadata": item["metadata"],
            "user_session": session,
            "created_at": current_time,
            "updated_at": current_time,
        }


class UserNotInterestedSeed(BaseSeed):
    raw_file = "users_not_interested"
    model = UserNotInterested
    dependencies = [
        CustomUserSeed,
        StorySeed,
    ]

    @classmethod
    def get_fields(cls, item):
        current_time = timezone.now().isoformat()
        return {
            "user": item["user"],
            "story": item["story"],
            "reason": item["reason"],
            "created_at": current_time,
            "updated_at": current_time,
        }


class AccessibilityToolSeed(BaseSeed):
    raw_file = "accessibility_tools"
    model = AccessibilityTool
    dependencies = [
        CustomUserSeed,
    ]

    @classmethod
    def get_fields(cls, item):
        current_time = timezone.now().isoformat()
        return {
            "user": item["user"],
            "tool_name": item["tool_name"],
            "created_at": current_time,
            "updated_at": current_time,
        }


# analytics/seeds.py
