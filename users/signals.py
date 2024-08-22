from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserFeedPosition  # users/views.py
from .utils import create_default_settings




@receiver(post_save, sender=CustomUser)
def create_user_settings(sender, instance, created, **kwargs):
    if created:  # and instance.is_active
        create_default_settings(instance)


@receiver(post_save, sender=CustomUser)
def create_user_feed_position(sender, instance, created, **kwargs):
    if created:
        UserFeedPosition.objects.create(user=instance)


# users/signals.py
