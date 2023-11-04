from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from utils.models import SoftDeletableModel, TimestampedModel

REPORT_CHOICES = [
    ('rumour', 'Rumour'),
    ('spam', 'Spam'),
    ('inappropriate', 'Inappropriate'),
    ('other', 'Other'),
]

class Report(SoftDeletableModel, TimestampedModel):
    """
    Model to represent reports or flags raised by users.
    """
    user = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    report_type = models.CharField(max_length=15, choices=REPORT_CHOICES)
    description = models.TextField(blank=True, null=True)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"Report by {self.user.email if self.user else 'Anonymous'} for {self.content_object}"


    def check_threshold_and_take_action(self):
        THRESHOLD = 5  # Set your desired threshold value here
        related_reports = Report.objects.filter(content_type=self.content_type, object_id=self.object_id)
        
        if related_reports.count() >= THRESHOLD:
            # Take action on the content_object
            # For example, you can set an 'is_flagged' attribute to True
            self.content_object.is_flagged = True
            self.content_object.save()

    class Meta:
        app_label = 'feedback'

# feedback/models.py 