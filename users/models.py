from django.db import models
from django.conf import settings
from django.db.models import JSONField
from authentication.models import CustomUser
# from stories.models import Story
from utils.models import SoftDeletableModel, TimestampedModel

class UserSetting(SoftDeletableModel, TimestampedModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='settings')
    system_settings = JSONField()
    account_settings = JSONField()
    notification_settings = JSONField()
    personal_settings = JSONField()

    class Meta:
        verbose_name = "User Setting"
        verbose_name_plural = "Users Setting"

    def __str__(self):
        return f"{self.user.email}'s Settings"

class UserFeedPosition(TimestampedModel):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    last_story_read = models.ForeignKey('stories.Story', on_delete=models.SET_NULL, null=True)


    def update_position(self, story):
        self.last_story_read = story
        self.save()


# TODO: it needs to be only created at not updated at.
class Follow(SoftDeletableModel, TimestampedModel):
    follower = models.ForeignKey(CustomUser, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(CustomUser, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Follower"
        verbose_name_plural = "Followers"
        unique_together = ('follower', 'followed')
        indexes = [
            models.Index(fields=['follower']),
            models.Index(fields=['followed']),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"
# users/models.py
