from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from .managers import SoftDeleteManager

class SoftDeletableModel(models.Model):
    """
    An abstract base class model with a `deleted_at` field and
    a custom manager for soft-deletion functionality.
    """
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = SoftDeleteManager()

    class Meta:
        abstract = True

    def soft_delete(self):
        """
        Soft delete the model instance.
        """
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """
        Restore a soft-deleted model instance.
        """
        self.deleted_at = None
        self.save()

    def hard_delete(self):
        """
        Permanently remove the model instance from the database.
        """
        super(SoftDeletableModel, self).delete()

    # If you want to add a custom manager method to fetch only deleted items
    @classmethod
    def deleted_objects(cls):
        return cls.objects.exclude(deleted_at__isnull=True)


class TimestampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    `created_at` and `updated_at` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class FlaggedContentMixin(models.Model):
    is_flagged = models.BooleanField(default=False, help_text="Indicates whether the content has been flagged due to crossing the report threshold.")

    class Meta:
        abstract = True

    def check_and_update_flag_status(self):
        from feedback.models import Report  # Avoid circular imports
        THRESHOLD = 5
        related_reports = Report.objects.filter(content_type=ContentType.objects.get_for_model(self), object_id=self.id)
        
        if related_reports.count() >= THRESHOLD:
            self.is_flagged = True
            self.save()

# utils/models.py