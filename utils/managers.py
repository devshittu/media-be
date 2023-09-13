from django.db import models

class ActiveManager(models.Manager):
    def active(self):
        return self.filter(deleted_at__isnull=True)
