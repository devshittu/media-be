from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, UserSetting

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
            "favorite_categories": ['__all__'],
        }
    }
    return UserSetting.objects.create(user=user, **default_settings)


@receiver(post_save, sender=CustomUser)
def create_user_settings(sender, instance, created, **kwargs):
    if created: # and instance.is_active
        create_default_settings(instance)