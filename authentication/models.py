from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save


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

class CustomUser(AbstractUser):
    """
    Custom user model that matches the provided data structure.
    """
    # The 'id' field is already provided by Django's base model.
    # The 'username' and 'email' fields are already provided by AbstractUser.
    
    name = models.CharField(max_length=255)  # New field for the full name of the user.
    
    # 'created_at' and 'updated_at' can be handled by Django's built-in timestamp fields.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 'last_login' is already provided by AbstractUser.
    
    # For roles, we can use a ManyToMany relationship with a Role model.
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
    # roles = models.ManyToManyField('Role', related_name='users')
    
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




class Role(models.Model):
    """
    Model to represent user roles.
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name



@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to handle tasks after a user is created or updated.
    For instance, sending a welcome email, or updating related models.
    """
    if created:
        # Send a welcome email or perform other tasks when a new user is created.
        pass
    else:
        # Handle tasks when a user's details are updated.
        pass

# authentication/models.py