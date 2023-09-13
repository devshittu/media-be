from django.db import models
from django.utils import timezone
from .managers import ActiveManager

class SoftDeletableModel(models.Model):
    """
    An abstract base class model with a `deleted_at` field and
    a custom manager for soft-deletion functionality.
    """
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    objects = ActiveManager()

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
