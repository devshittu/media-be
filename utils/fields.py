from rest_framework.fields import DateTimeField
import time

class UnixTimestampDateTimeField(DateTimeField):
    """
    Represent a `DateTimeField` as a UNIX timestamp.
    """

    def to_representation(self, value):
        """
        Convert the datetime to a UNIX timestamp.
        """
        return int(time.mktime(value.timetuple()))

# utils/fields.py