from django.db import models
from django.conf import settings
from autoslug import AutoSlugField
from utils.models import SoftDeletableModel, TimestampedModel, FlaggedContentMixin


class Category(SoftDeletableModel, TimestampedModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from="name", unique=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subcategories",
    )


class Ticket(SoftDeletableModel, TimestampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()


class TicketResponse(SoftDeletableModel, TimestampedModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    message = models.TextField()


class Tag(SoftDeletableModel, TimestampedModel):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(
        populate_from="name", unique=True, always_update=True, db_index=True
    )


class AppVersion(SoftDeletableModel, TimestampedModel):
    version = models.CharField(max_length=50, unique=True)
    major_version = models.IntegerField()
    minor_version = models.IntegerField()
    features = models.TextField(blank=True)
    updates = models.TextField(blank=True)
    bug_fixes = models.TextField(blank=True)
    deprecations = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Automatically set major and minor version fields
        major, minor, _ = self.version.split(".", 2)
        self.major_version = int(major)
        self.minor_version = int(minor)
        super().save(*args, **kwargs)


class Article(SoftDeletableModel, TimestampedModel):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(
        populate_from="title", unique=True, always_update=True, db_index=True
    )
    content = models.TextField(help_text="Content in Markdown format")
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )
    tags = models.ManyToManyField(Tag, related_name="articles")
    app_version = models.ForeignKey(
        AppVersion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
    )


class FAQ(SoftDeletableModel, TimestampedModel):
    question = models.CharField(max_length=255)
    answer = models.TextField(help_text="Answer in Markdown format")
    app_version = models.ForeignKey(
        AppVersion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="faqs",
    )


class VersionedDocument(SoftDeletableModel, TimestampedModel):
    content = models.TextField(help_text="Content in Markdown format")
    # app_version = models.ForeignKey(
    #     AppVersion,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="faqs",
    # )

    class Meta:
        abstract = True


class TermsAndConditions(VersionedDocument):
    title = models.CharField(max_length=255)
    app_version = models.ForeignKey(
        AppVersion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="terms_and_conditions",  # Unique related_name
    )


class PrivacyPolicy(VersionedDocument):
    title = models.CharField(max_length=255)
    app_version = models.ForeignKey(
        AppVersion,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="privacy_policy",  # Updated related_name
    )


# support/models.py
