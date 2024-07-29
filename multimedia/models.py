import logging
import os
from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
import imageio
from pydub import AudioSegment
from django.core.exceptions import ValidationError
from utils.models import SoftDeletableModel, TimestampedModel
from django.core.files.storage import default_storage

# Set up the logger for this module
logger = logging.getLogger('app_logger')


def validate_file_size(value):
    """Validate the size of the uploaded file."""
    logger.debug('Validating file size')
    filesize = value.size

    if filesize > 10485760:  # 10MB
        logger.warning('File size exceeds 10MB')
        raise ValidationError(
            "The maximum file size that can be uploaded is 10MB")
    else:
        return value


def validate_file_extension(value):
    """Validate the file extension of the uploaded file."""
    logger.debug('Validating file extension')
    ext = os.path.splitext(value.name)[1]
    valid_extensions = [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".mp3"]
    if not ext.lower() in valid_extensions:
        logger.warning('Unsupported file extension')
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
    # URL for the file's avatar.
    media_url = models.URLField(blank=True, null=True)
    caption = models.CharField(
        max_length=100, blank=True, null=True
    )

    thumbnail = models.ImageField(
        upload_to="thumbnails/", null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    story = models.ForeignKey(
        "stories.Story", related_name="multimedia", on_delete=models.CASCADE
    )

    def optimize_multimedia(self):
        """Optimize the multimedia file."""
        logger.debug('Optimizing multimedia file')
        if self.media_type == "photo":
            with default_storage.open(self.file.name, "rb") as f:
                img = Image.open(f)
                img = img.convert("RGB")
                if img.height > 3000 or img.width > 3000:
                    output_size = (3000, 3000)
                    img.thumbnail(output_size)
                img.save(self.file.path, "JPEG")
                logger.info(f"Optimized photo for {self.file.name}")

        elif self.media_type == "audio":
            audio = AudioSegment.from_file(self.file.path, format="mp3")
            audio = audio.set_channels(1).set_frame_rate(22050)
            audio.export(self.file.path, format="mp3", bitrate="64k")
            logger.info(f"Optimized audio for {self.file.name}")

    def create_thumbnail(self):
        """Generate a thumbnail for the multimedia."""
        logger.debug('Creating thumbnail for multimedia')
        if self.media_type == "photo":
            with default_storage.open(self.file.name, "rb") as f:
                img = Image.open(f)
                img.thumbnail((300, 300))
                thumbnail_path = self.file.name.replace(
                    "media_files", "thumbnails")
                img.save(default_storage.path(thumbnail_path), "JPEG")
                self.thumbnail.save(
                    thumbnail_path.split("/")[-1],
                    default_storage.open(thumbnail_path, "rb"),
                )
                logger.info(f"Created thumbnail for photo {self.file.name}")

        elif self.media_type == "video":
            reader = imageio.get_reader(self.file.path)
            img_array = reader.get_next_data()
            img = Image.fromarray(img_array)
            img.thumbnail((300, 300))
            thumbnail_path = self.file.path.replace(
                "media_files", "thumbnails")
            img.save(thumbnail_path, "JPEG")
            self.thumbnail.save(
                thumbnail_path.split("/")[-1], open(thumbnail_path, "rb")
            )
            logger.info(f"Created thumbnail for video {self.file.name}")

    def save(self, *args, **kwargs):
        logger.debug('Saving multimedia instance')
        self.optimize_multimedia()
        self.create_thumbnail()
        super().save(*args, **kwargs)
        logger.info(f"Saved multimedia instance {self.id}")

    class Meta:
        verbose_name = "Story Multimedia"
        verbose_name_plural = "Stories Multimedia"

    def __str__(self):
        return f"{self.media_type} by {self.user.email} for story {self.story.id}"


# multimedia/models.py
