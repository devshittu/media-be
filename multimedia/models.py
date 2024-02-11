from django.db import models
from django.contrib.auth import get_user_model

from django.conf import settings
from django.core.exceptions import ValidationError
from utils.models import SoftDeletableModel, TimestampedModel
from django.core.files.storage import default_storage

# from utils.validations import validate_json
# import json
from .tasks import (
    process_multimedia,
)


def validate_file_size(value):
    """Validate the size of the uploaded file."""
    filesize = value.size

    if filesize > 10485760:  # 10MB
        raise ValidationError("The maximum file size that can be uploaded is 10MB")
    else:
        return value


def validate_file_extension(value):
    """Validate the file extension of the uploaded file."""
    import os

    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mp3"]
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension.")


MEDIA_CHOICES = [
    ("video", "Video"),
    ("audio", "Audio Note"),
    ("gif", "GIF"),
    ("photo", "Photo"),
]


class Multimedia(SoftDeletableModel, TimestampedModel):
    """
    Multimedia model to store media associated with stories.
    """

    file = models.FileField(
        upload_to="media_files/",
        validators=[validate_file_size, validate_file_extension],
        blank=True,
        null=True,
    )
    media_url = models.URLField(blank=True, null=True)  # URL for the file's avatar.
    caption = models.CharField(max_length=100, blank=True, null=True)

    thumbnail = models.ImageField(upload_to="thumbnails/", null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    story = models.ForeignKey(
        "stories.Story", related_name="multimedia", on_delete=models.CASCADE
    )
    metadata = models.JSONField(blank=True, null=True)

    # def save(self, *args, **kwargs):
    #     # Flag to check if the instance is newly created
    #     is_new = self._state.adding
    #     super().save(*args, **kwargs)  # Save the instance first to get an ID

    #     # If the media is newly added, process it accordingly
    #     if is_new:
    #         if self.media_type == "audio":
    #             generate_waveform.delay(self.id)
    #         # Call tasks for optimization and thumbnail generation
    #         optimize_media.delay(self.id)
    #         create_thumbnail.delay(self.id)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            process_multimedia.delay(self.id)

            # Update media_url after multimedia processing is complete
            self.media_url = self.get_media_url()
            self.save(update_fields=["media_url"])  # Update only media_url field

    def get_media_url(self):
        if self.file:
            return self.file.url
            # return settings.BASE_URL + self.file.url
        return None

    class Meta:
        verbose_name = "Story Multimedia"
        verbose_name_plural = "Stories Multimedia"

    def __str__(self):
        return f"{self.media_type} by {self.user.email} for story {self.story.id}"


# multimedia/models.py
