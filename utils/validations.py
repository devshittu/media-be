# utils/validations.py

import json
from django.core.exceptions import ValidationError


def validate_json(data):
    try:
        if data == "":
            return {}  # or None, based on your requirement
        return json.loads(data)
    except ValueError as e:
        raise ValidationError(f"Invalid JSON data: {e}")
