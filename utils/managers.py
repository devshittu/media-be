from django.db import models

class SoftDeleteManager(models.Manager):
    def active(self):
        return self.filter(deleted_at__isnull=True)

    def deleted(self):
        return self.filter(deleted_at__isnull=False)


class ActiveUnflaggedManager(models.Manager):
    def active_and_unflagged(self):
        return self.filter(deleted_at__isnull=True, is_flagged=False)
