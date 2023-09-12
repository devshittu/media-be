from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.postgres.fields import JSONField
import time
from django.db.models.signals import post_save
from django.dispatch import receiver

# Custom user manager for email-based authentication
class CustomUserManager(BaseUserManager):
    """
    Custom manager for User model with email as the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a User with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Custom user model for email-based authentication
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model where email is the unique identifier
    and has an is_admin field to grant admin rights.
    Password and email fields are required. Other fields are optional.
    """
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    roles = models.JSONField(default=list)  # Store roles as a JSON list
    avatar_url = models.URLField(blank=True, null=True)
    # news_channel = models.ForeignKey('NewsChannel', on_delete=models.SET_NULL, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

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
    return Setting.objects.create(user=user, **default_settings)

class Setting(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE, related_name='settings')
    system_settings = JSONField()
    account_settings = JSONField()
    notification_settings = JSONField()
    personal_settings = JSONField()
    created_at = models.BigIntegerField(default=lambda: int(time.time()))
    updated_at = models.BigIntegerField(default=lambda: int(time.time()))

    def __str__(self):
        return f"{self.user.email}'s Settings"
    
    def save(self, *args, **kwargs):
        self.updated_at = int(time.time())
        super().save(*args, **kwargs)

    
@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        create_default_settings(instance)

# users/models.py
