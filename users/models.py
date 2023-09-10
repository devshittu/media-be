from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

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
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # User settings
    preferred_categories = models.ManyToManyField('Category', related_name='users')
    language = models.CharField(max_length=10, default='en')
    theme = models.CharField(max_length=10, default='light')

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Settings(models.Model):
    """
    Model to store user settings.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')
    preferred_categories = models.ManyToManyField('Category', related_name='settings')
    language = models.CharField(max_length=10, default='en')
    theme = models.CharField(max_length=10, default='light')

    def __str__(self):
        return f"{self.user.email}'s Settings"