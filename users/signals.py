from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserSetting, UserFeedPosition


def create_default_settings(user):
    default_settings = {
        "system_settings": {"theme": "system", "language": "en"},
        "account_settings": {
            "username": user.username,
            "display_name": user.display_name,
            "email": user.email,
        },
        "notification_settings": {
            "email": {
                "account": True,
                "marketing": True,
                "updates": True,
            },
        },
        "personal_settings": {
            "favorite_categories": ["__all__"],
        },
    }
    return UserSetting.objects.create(user=user, **default_settings)


@receiver(post_save, sender=CustomUser)
def create_user_settings(sender, instance, created, **kwargs):
    if created:  # and instance.is_active
        create_default_settings(instance)


@receiver(post_save, sender=CustomUser)
def create_user_feed_position(sender, instance, created, **kwargs):
    if created:
        UserFeedPosition.objects.create(user=instance)


# users/signals.py
