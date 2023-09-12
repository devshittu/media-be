from django.db import models
from django.conf import settings
from django.contrib.postgres.fields import JSONField  # Assuming you're using PostgreSQL

class DeviceData(models.Model):
    """
    Model to track device and technical data.
    """
    interaction = models.OneToOneField('StoryInteraction', on_delete=models.CASCADE, related_name='device_data')
    device_type = models.CharField(max_length=50)
    operating_system = models.CharField(max_length=50)
    browser = models.CharField(max_length=50)
    screen_resolution = models.CharField(max_length=50)
    connection_type = models.CharField(max_length=50)

    def __str__(self):
        return f"Device data for interaction: {self.interaction.id}"

class LocationData(models.Model):
    """
    Model to track user location data.
    """
    interaction = models.OneToOneField('StoryInteraction', on_delete=models.CASCADE, related_name='location_data')
    ip_address = models.GenericIPAddressField()
    geolocation = models.CharField(max_length=255)  # This could be further normalized if needed
    time_zone = models.CharField(max_length=50)

    def __str__(self):
        return f"Location data for interaction: {self.interaction.id}"

class ReferralData(models.Model):
    """
    Model to track referral data.
    """
    interaction = models.OneToOneField('StoryInteraction', on_delete=models.CASCADE, related_name='referral_data')
    referrer_url = models.URLField()
    search_terms = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Referral data for interaction: {self.interaction.id}"

class UserSession(models.Model):
    """
    Model to represent a user's session.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sessions')
    session_id = models.UUIDField(unique=True)  # Unique identifier for the session
    device_data = models.OneToOneField(DeviceData, on_delete=models.CASCADE, related_name='session')
    location_data = models.OneToOneField(LocationData, on_delete=models.CASCADE, related_name='session')
    start_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_id} for {self.user}"

class StoryInteraction(models.Model):
    """
    Generic model to track various interactions with stories.
    """
    INTERACTION_CHOICES = [
        ('view', 'View'),
        ('bookmark', 'Bookmark'),
        ('unbookmark', 'Unbookmark'),
        ('share', 'Share'),
        ('click_external', 'Click External Link'),
        ('view_timeline', 'View Story Timeline'),
        # ... other interactions ...
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='story_interactions')
    story = models.ForeignKey('stories.Story', on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=50, choices=INTERACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    metadata = JSONField(blank=True, null=True)  # Additional data for the interaction
    session = models.ForeignKey(UserSession, on_delete=models.CASCADE, related_name='interactions')
    #     scroll_depth = models.PositiveIntegerField(null=True)  # Represented as a percentage
#     highlighted_text = models.TextField(blank=True, null=True)
    

    class Meta:
        verbose_name = 'Story Interaction'
        verbose_name_plural = 'Story Interactions'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} {self.interaction_type} {self.story} on {self.timestamp}"

class UserNotInterested(models.Model):
    """
    Model to track stories users are not interested in.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uninterested_stories')
    story = models.ForeignKey('stories.Story', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)  # Optional field if you want to capture why they're not interested

    class Meta:
        verbose_name = 'User Not Interested'
        verbose_name_plural = 'Users Not Interested'
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} not interested in {self.story} on {self.timestamp}"


class AccessibilityTool(models.Model):
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
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Accessibility Tool'
        verbose_name_plural = 'Accessibility Tools'

    def __str__(self):
        return f"{self.user} used {self.tool_name} on {self.timestamp}"
# analytics/models.py