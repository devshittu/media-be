from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image
import imageio
from pydub import AudioSegment
from django.core.exceptions import ValidationError
from utils.models import SoftDeletableModel

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
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mp3']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')


MEDIA_CHOICES = [
    ('video', 'Video'),
    ('audio', 'Audio Note'),
    ('gif', 'GIF'),
    ('photo', 'Photo'),
]

class Multimedia(SoftDeletableModel):
    """
    Multimedia model to store media associated with posts.
    """
    file = models.FileField(upload_to='media_files/', validators=[validate_file_size, validate_file_extension])
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)
    media_type = models.CharField(max_length=10, choices=MEDIA_CHOICES)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey('posts.Post', related_name='multimedia', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def optimize_multimedia(self):
        """Optimize the multimedia file."""
        if self.media_type == 'photo':
            img = Image.open(self.file.path)
            img = img.convert('RGB')
            if img.height > 3000 or img.width > 3000:
                output_size = (3000, 3000)
                img.thumbnail(output_size)
            img.save(self.file.path, 'JPEG')

        elif self.media_type == 'audio':
            audio = AudioSegment.from_file(self.file.path, format="mp3")
            audio = audio.set_channels(1).set_frame_rate(22050)
            audio.export(self.file.path, format="mp3", bitrate="64k")

    def create_thumbnail(self):
        """Generate a thumbnail for the multimedia."""
        if self.media_type == 'photo':
            img = Image.open(self.file.path)
            img.thumbnail((300, 300))
            thumbnail_path = self.file.path.replace("media_files", "thumbnails")
            img.save(thumbnail_path, "JPEG")
            self.thumbnail.save(
                thumbnail_path.split('/')[-1], 
                open(thumbnail_path, 'rb')
            )

        elif self.media_type == 'video':
            reader = imageio.get_reader(self.file.path)
            img_array = reader.get_next_data()
            img = Image.fromarray(img_array)
            img.thumbnail((300, 300))
            thumbnail_path = self.file.path.replace("media_files", "thumbnails")
            img.save(thumbnail_path, "JPEG")
            self.thumbnail.save(
                thumbnail_path.split('/')[-1], 
                open(thumbnail_path, 'rb')
            )

    def save(self, *args, **kwargs):
        self.optimize_multimedia()
        self.create_thumbnail()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.media_type} by {self.user.email} for post {self.post.id}"
