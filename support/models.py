import re
from django.db import models
from django.conf import settings
from django.utils.html import strip_tags
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

    def __str__(self):
        return self.name


class Ticket(SoftDeletableModel, TimestampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.subject


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

    def __str__(self):
        return self.name


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

    def __str__(self):
        return self.version


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

    def __str__(self):
        return self.title

    def summary(self):
        """
        Generate a summary of the content, not exceeding 200 characters.
        """
        content_text = self._strip_markdown(strip_tags(self.content))
        max_length = 200

        if len(content_text) > max_length:
            return content_text[:max_length].rsplit(" ", 1)[0] + "..."
        else:
            return content_text

    def reading_time(self):
        """
        Calculate the reading time of the article, stripping HTML and Markdown syntax.
        Assumes an average reading speed of 200 words per minute.
        """
        content_text = self._strip_markdown(strip_tags(self.content))
        word_count = len(re.findall(r"\w+", content_text))
        reading_speed_per_minute = 200
        reading_time_minutes = word_count / reading_speed_per_minute
        return max(1, round(reading_time_minutes))  # Ensure at least 1 minute

    def _strip_markdown(self, text):
        """
        Strip Markdown syntax elements from text.
        """
        # Patterns with capturing groups
        patterns_with_groups = [
            (r"\!\[.*?\]\(.*?\)", ""),  # Images
            (r"\[.*?\]\(.*?\)", ""),  # Links
            (r"\*\*(.*?)\*\*", r"\1"),  # Bold
            (r"\*(.*?)\*", r"\1"),  # Italic
            (r"\~\~(.*?)\~\~", r"\1"),  # Strikethrough
            (r"\`(.*?)\`", r"\1"),  # Inline code
        ]

        # Patterns without capturing groups
        patterns_without_groups = [
            r"\n\-(.*?)",  # List items
            r"\n\*(.*?)",  # List items
            r"\n\d\.(.*?)",  # Numbered list items
            r"\#\s(.*?)",  # Headers
            r"\>\s(.*?)",  # Blockquotes
        ]

        for pattern, replacement in patterns_with_groups:
            text = re.sub(pattern, replacement, text)

        for pattern in patterns_without_groups:
            text = re.sub(pattern, "", text)

        # Remove any remaining Markdown characters
        text = re.sub(r"[\*\[\]\(\)\#\>\`\-\!\~]", "", text)

        return text


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
