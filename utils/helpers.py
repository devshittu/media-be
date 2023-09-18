import datetime
from django.utils import timezone

def unix_to_datetime(unix_timestamp):
    # Convert the Unix timestamp to a naive datetime object
    naive_datetime = datetime.datetime.utcfromtimestamp(unix_timestamp)
    
    # Make the datetime object timezone-aware
    aware_datetime = timezone.make_aware(naive_datetime, timezone=timezone.utc)
    
    return aware_datetime

# utils/helpers.py