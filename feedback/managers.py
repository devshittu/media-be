from django.db import models

class ReportManager(models.Manager):
    def unflagged(self):
        return self.filter(is_flagged=False)

    def flagged(self):
        return self.filter(is_flagged=True)
