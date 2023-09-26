from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from utils.models import TimestampedModel
from datetime import timedelta
from system_messaging.utils import send_message
from decouple import config
from datetime import timedelta
from django.utils import timezone

# Third-party Imports
from decouple import config

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

    def not_followed_by(self, user):
        # Get all user IDs that the given user is following
        followed_ids = user.following.values_list('followed_id', flat=True)
        
        # Exclude those users from the main user queryset
        return self.exclude(id__in=followed_ids).exclude(id=user.id)
    

class CustomUser(AbstractUser):
    """
    Custom user model that matches the provided data structure.
    """
    # The 'id' field is already provided by Django's base model.
    # The 'username' and 'email' fields are already provided by AbstractUser.
    
    name = models.CharField(max_length=255)  # New field for the full name of the user.
    
    ROLE_CHOICES = [
        ('reader', 'Reader'),
        ('writer', 'Writer'),
        ('editor', 'Editor'),
        ('reviewer', 'Reviewer'),
        ('publisher', 'Publisher'),
    ]
    roles = ArrayField(
        models.CharField(max_length=10, choices=ROLE_CHOICES),
        default=list,
        blank=True
    )
    email = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=30, unique=True)
    avatar_url = models.URLField(blank=True, null=True)  # URL for the user's avatar.
    display_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    last_activity = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    has_completed_setup = models.BooleanField(default=False, null=True, blank=True)
   
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email
    
    def update_last_activity(self):
        """
        Update the last activity timestamp for the user.
        """
        self.last_activity = timezone.now()
        self.save()

    class Meta:
        verbose_name_plural = "Users"

class PasswordResetToken( TimestampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(hours=24)  # Token is valid for 24 hours


class OTP(TimestampedModel):  # Assuming TimestampedModel is a base model with created_at and updated_at fields
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='otps')
    otp = models.CharField(max_length=8)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def is_valid(self):
        # return not self.is_used and datetime.now() < self.expires_at
        return not self.is_used and timezone.now() < self.expires_at


class VerificationToken(TimestampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return timezone.now() < self.expires_at

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500)
    blacklisted_at = models.DateTimeField(auto_now_add=True)


# authentication/models.py