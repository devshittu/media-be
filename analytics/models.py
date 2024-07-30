import logging
from django.db import models
from django.conf import settings
from django.db.models import JSONField
from utils.models import SoftDeletableModel, TimestampedModel

# Set up the logger for this module
logger = logging.getLogger('app_logger')


class UserSession(SoftDeletableModel, TimestampedModel):
    """
    Model to represent a user's session.
    """
    logger.debug('Initializing UserSession model')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_sessions"
    )
    # Unique identifier for the session
    session_token = models.UUIDField(unique=True)
    # location_data
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    geolocation = models.CharField(
        max_length=255, null=True, blank=True
    )  # This could be further normalized if needed
    time_zone = models.CharField(max_length=50, null=True, blank=True)
    # device_data
    device_type = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
    screen_resolution = models.CharField(max_length=50, null=True, blank=True)
    connection_type = models.CharField(max_length=50, null=True, blank=True)

    start_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "User Session"
        verbose_name_plural = "User Sessions"

    def __str__(self):
        logger.debug(
            f'Returning string representation for session {self.session_token}')
        return f"Session {self.session_token} for {self.user}"


class StoryInteraction(SoftDeletableModel, TimestampedModel):
    """
    Generic model to track various interactions with stories.
    """
    logger.debug('Initializing StoryInteraction model')

    INTERACTION_CHOICES = [
        ("view", "View"),
        ("add-bookmark", "Add Bookmark"),
        ("remove-bookmark", "Remove Bookmark"),
        ("update-bookmark", "Update Bookmark"),
        ("add-like", "Add Like"),
        ("remove-like", "Remove Like"),
        ("add-dislike", "Add Dislike"),
        ("remove-dislike", "Remove Dislike"),
        ("share", "Share"),
        ("click_external", "Click External Link"),
        ("view_storyline", "View Storyline"),
        ("report", "Report"),
        ("highlight_text", "Highlight Text"),
        # ... other interactions as needed ...
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="story_interactions",
        null=True,
        blank=True,
    )
    story = models.ForeignKey(
        "stories.Story", on_delete=models.CASCADE, related_name="interactions"
    )
    interaction_type = models.CharField(
        max_length=50, choices=INTERACTION_CHOICES)
    # Additional data for the interaction
    metadata = JSONField(blank=True, null=True)
    user_session = models.ForeignKey(
        UserSession,
        on_delete=models.CASCADE,
        related_name="interactions",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Story Interaction"
        verbose_name_plural = "Stories Interactions"

    def __str__(self):
        logger.debug(
            f'Returning string representation for interaction {self.id}')
        return f"{self.user} {self.interaction_type} {self.story} on {self.created_at}"


class StoryInteractionMetadataSchema(SoftDeletableModel, TimestampedModel):
    logger.debug('Initializing StoryInteractionMetadataSchema model')
    interaction_type = models.CharField(
        max_length=50, choices=StoryInteraction.INTERACTION_CHOICES
    )
    version = models.CharField(max_length=10)
    schema = JSONField()

    class Meta:
        unique_together = ("interaction_type", "version")

    def __str__(self):
        logger.debug(
            f'Returning string representation for metadata schema {self.id}')
        return f"{self.interaction_type} v{self.version}"


class UserNotInterested(SoftDeletableModel, TimestampedModel):
    """
    Model to track stories users are not interested in.
    """
    logger.debug('Initializing UserNotInterested model')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="uninterested_stories",
    )
    story = models.ForeignKey("stories.Story", on_delete=models.CASCADE)
    reason = models.TextField(
        blank=True, null=True
    )  # Optional field if you want to capture why they're not interested

    class Meta:
        verbose_name = "User Not Interested"
        verbose_name_plural = "Users Not Interested"
        ordering = ["-created_at"]

    def __str__(self):
        logger.debug(
            f'Returning string representation for uninterested story {self.id}')
        return f"{self.user} not interested in {self.story} on {self.created_at}"


class AccessibilityTool(SoftDeletableModel, TimestampedModel):
    """
    Model to track accessibility tools used.
    """
    logger.debug('Initializing AccessibilityTool model')

    TOOL_CHOICES = [
        ("screen_reader", "Screen Reader"),
        ("magnifier", "Magnifier"),
        # ... other tools ...
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="accessibility_tools",
    )
    tool_name = models.CharField(max_length=100, choices=TOOL_CHOICES)

    class Meta:
        verbose_name = "Accessibility Tool"
        verbose_name_plural = "Accessibility Tools"

    def __str__(self):
        logger.debug(
            f'Returning string representation for accessibility tool {self.id}')
        return f"{self.user} used {self.tool_name} on {self.created_at}"


# analytics/models.py
