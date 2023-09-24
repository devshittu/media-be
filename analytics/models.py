from django.db import models
from django.conf import settings
from django.db.models import JSONField
from utils.models import SoftDeletableModel, TimestampedModel

class UserSession(SoftDeletableModel, TimestampedModel):
    """
    Model to represent a user's session.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_sessions')
    session_token = models.UUIDField(unique=True)  # Unique identifier for the session
    # location_data 
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    geolocation = models.CharField(max_length=255, null=True, blank=True)  # This could be further normalized if needed
    time_zone = models.CharField(max_length=50, null=True, blank=True)
    # device_data 
    device_type = models.CharField(max_length=50, null=True, blank=True)
    operating_system = models.CharField(max_length=50, null=True, blank=True)
    browser = models.CharField(max_length=50, null=True, blank=True)
    screen_resolution = models.CharField(max_length=50, null=True, blank=True)
    connection_type = models.CharField(max_length=50, null=True, blank=True)

    start_timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'User Session'
        verbose_name_plural = 'User Sessions'

    def __str__(self):
        return f"Session {self.session_id} for {self.user}"


class StoryInteraction(SoftDeletableModel, TimestampedModel):
    """
    Generic model to track various interactions with stories.
    """
    INTERACTION_CHOICES = [
        ('view', 'View'),
        ('bookmark', 'Bookmark'),
        ('unbookmark', 'Unbookmark'),
        ('share', 'Share'),
        ('click_external', 'Click External Link'),
        ('view_storyline', 'View Storyline'),
        ('report', 'Report story'),
        ('highlight_text', 'Highlight Text'),
        # ... other interactions ...
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='story_interactions')
    story = models.ForeignKey('stories.Story', on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_CHOICES)
    metadata = JSONField(blank=True, null=True)  # Additional data for the interaction
    user_session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='interactions')

    class Meta:
        verbose_name = 'Story Interaction'
        verbose_name_plural = 'Stories Interactions'

    def __str__(self):
        return f"{self.user} {self.interaction_type} {self.story} on {self.created_at}"


class StoryInteractionMetadataSchema(SoftDeletableModel, TimestampedModel):
    interaction_type = models.CharField(max_length=50, choices=StoryInteraction.INTERACTION_CHOICES)
    version = models.CharField(max_length=10)
    schema = JSONField()

    class Meta:
        unique_together = ('interaction_type', 'version')


class UserNotInterested(SoftDeletableModel, TimestampedModel):
    """
    Model to track stories users are not interested in.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uninterested_stories')
    story = models.ForeignKey('stories.Story', on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)  # Optional field if you want to capture why they're not interested

    class Meta:
        verbose_name = 'User Not Interested'
        verbose_name_plural = 'Users Not Interested'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user} not interested in {self.story} on {self.created_at}"


class AccessibilityTool(SoftDeletableModel, TimestampedModel):
    """
    Model to track accessibility tools used.
    """
    TOOL_CHOICES = [
        ('screen_reader', 'Screen Reader'),
        ('magnifier', 'Magnifier'),
        # ... other tools ...
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accessibility_tools')
    tool_name = models.CharField(max_length=100, choices=TOOL_CHOICES)

    class Meta:
        verbose_name = 'Accessibility Tool'
        verbose_name_plural = 'Accessibility Tools'

    def __str__(self):
        return f"{self.user} used {self.tool_name} on {self.created_at}"

# analytics/models.py