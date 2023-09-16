from django.db import models
from django.conf import settings
from django.db.models import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import CustomUser
from utils.models import SoftDeletableModel, TimestampedModel


def create_default_settings(user):
    default_settings = {
        "system_settings": {"theme": "system", "language": "en"},
        "account_settings": {
            "display_name": user.username,
            "email": user.email,
        },
        "notification_settings": {
            "email": {
                "account": 1,
                "marketing": 1,
                "updates": 1,
            },
        },
        "personal_settings": {
            "favorite_categories": ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11'],
        }
    }
    return UserSetting.objects.create(user=user, **default_settings)

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
    

    
@receiver(post_save, sender=CustomUser)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        create_default_settings(instance)

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
