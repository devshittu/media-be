# users/utils.py

from .models import UserSetting


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
